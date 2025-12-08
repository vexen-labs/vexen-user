"""SQLAlchemy User model."""

import uuid
from datetime import datetime

from uuid6 import uuid7

from sqlalchemy import JSON, DateTime, String, TypeDecorator, event, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class UUIDType(TypeDecorator):
	"""Platform-independent UUID type that stores as string."""

	impl = String
	cache_ok = True

	def process_bind_param(self, value, dialect):
		"""Convert UUID to string for database storage."""
		if value is None:
			return None
		if isinstance(value, uuid.UUID):
			return str(value)
		# Try to convert string to UUID first to validate
		try:
			return str(uuid.UUID(str(value)))
		except (ValueError, AttributeError):
			return None

	def process_result_value(self, value, dialect):
		"""Convert string back to UUID when retrieving from database."""
		if value is None:
			return None
		if isinstance(value, uuid.UUID):
			return value
		try:
			return uuid.UUID(value)
		except (ValueError, AttributeError, TypeError):
			return None


class Base(DeclarativeBase):
	pass


class UserModel(Base):
	"""User table model"""

	__tablename__ = "users"

	id: Mapped[uuid.UUID] = mapped_column(UUIDType, primary_key=True, nullable=False)
	email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
	name: Mapped[str] = mapped_column(String, nullable=False)
	avatar: Mapped[str | None] = mapped_column(String, nullable=True)
	status: Mapped[str] = mapped_column(String, nullable=False, default="active", index=True)
	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True), server_default=func.now(), nullable=False
	)
	updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
	last_login: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
	user_metadata: Mapped[dict | None] = mapped_column(JSON, nullable=True)


# Generate UUID v7 for new users before insert
@event.listens_for(UserModel, "before_insert")
def generate_uuid(mapper, connection, target):
	"""Generate UUID v7 for new users if not provided."""
	if target.id is None:
		target.id = uuid7()
