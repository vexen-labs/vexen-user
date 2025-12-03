"""DTOs for User operations."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserResponse:
	"""Standard user response for list operations"""

	id: str
	email: str
	name: str
	avatar: str | None
	status: str
	created_at: datetime
	last_login: datetime | None


@dataclass
class UserExpandedResponse:
	"""Expanded user response with all details"""

	id: str
	email: str
	name: str
	avatar: str | None
	status: str
	created_at: datetime
	updated_at: datetime | None
	last_login: datetime | None
	user_metadata: dict


@dataclass
class CreateUserRequest:
	"""Request to create a new user"""

	email: str
	name: str
	password: str
	avatar: str | None = None
	user_metadata: dict | None = None


@dataclass
class UpdateUserRequest:
	"""Request to update user (PUT - all fields)"""

	name: str | None = None
	avatar: str | None = None
	status: str | None = None
	user_metadata: dict | None = None


@dataclass
class PatchUserRequest:
	"""Request to partially update user (PATCH)"""

	name: str | None = None
	avatar: str | None = None
	status: str | None = None
	user_metadata: dict | None = None


@dataclass
class UserStatsResponse:
	"""User statistics"""

	total: int
	active: int
	inactive: int
	new_this_month: int
	recent_logins: int
