"""SQLAlchemy User External Identity model."""

import uuid
from datetime import datetime

from uuid6 import uuid7

from sqlalchemy import JSON, DateTime, ForeignKey, Index, String, event, func
from sqlalchemy.orm import Mapped, mapped_column

from .user import Base, UUIDType


class UserExternalIdentityModel(Base):
	"""
	User external identity table - links users to external OAuth/OpenID providers.

	This table stores the relationship between internal users and their identities
	from external authentication providers (Google, Azure, GitHub, etc.).

	Example:
		A user can have multiple external identities:
		- user_id: 018d-abc...  provider: 'google'   provider_user_id: '108012...'
		- user_id: 018d-abc...  provider: 'github'   provider_user_id: '1234567'
		- user_id: 018d-abc...  provider: 'azure'    provider_user_id: 'abc123...'
	"""

	__tablename__ = "user_external_identities"

	id: Mapped[uuid.UUID] = mapped_column(UUIDType, primary_key=True, nullable=False)
	user_id: Mapped[uuid.UUID] = mapped_column(
		UUIDType, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
	)

	# Provider information
	provider: Mapped[str] = mapped_column(
		String(50),
		nullable=False,
		index=True,
		comment="Provider name (google, azure, github, etc.)",
	)
	provider_user_id: Mapped[str] = mapped_column(
		String(255),
		nullable=False,
		comment="Unique user ID from the provider (the 'sub' claim from OpenID)",
	)

	# User information from provider
	email: Mapped[str | None] = mapped_column(
		String(255), nullable=True, comment="Email from the provider"
	)
	provider_data: Mapped[dict | None] = mapped_column(
		JSON,
		nullable=True,
		comment="Additional data from provider (name, picture, locale, etc.)",
	)

	# Timestamps
	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True), server_default=func.now(), nullable=False
	)
	updated_at: Mapped[datetime | None] = mapped_column(
		DateTime(timezone=True), onupdate=func.now(), nullable=True
	)

	__table_args__ = (
		# Each provider identity can only be linked to one user
		Index(
			"uq_provider_user_id",
			"provider",
			"provider_user_id",
			unique=True,
		),
	)


# Generate UUID v7 for new external identities before insert
@event.listens_for(UserExternalIdentityModel, "before_insert")
def generate_external_identity_uuid(mapper, connection, target):  # noqa: ARG001
	"""Generate UUID v7 for new external identities if not provided."""
	if target.id is None:
		target.id = uuid7()
