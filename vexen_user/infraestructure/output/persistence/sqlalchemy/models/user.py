"""SQLAlchemy User model."""

from datetime import datetime

from sqlalchemy import JSON, DateTime, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
	pass


class UserModel(Base):
	"""User table model"""

	__tablename__ = "users"

	id: Mapped[str] = mapped_column(String, primary_key=True)
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
