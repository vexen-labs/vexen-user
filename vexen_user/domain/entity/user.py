"""
User entity for the domain layer.
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
	"""
	User entity representing a system user.

	Attributes:
		id: Unique identifier (e.g., "usr_123456")
		email: User's email address
		name: User's full name
		avatar: URL to user's avatar image
		status: User status (active, inactive)
		created_at: Timestamp when user was created
		updated_at: Timestamp when user was last updated
		last_login: Timestamp of last login
		metadata: Additional user metadata (department, phone, etc.)
	"""

	id: str | None
	email: str
	name: str
	avatar: str | None = None
	status: str = "active"  # active, inactive
	created_at: datetime = field(default_factory=datetime.now)
	updated_at: datetime | None = None
	last_login: datetime | None = None
	metadata: dict | None = None

	def __post_init__(self):
		"""Validation"""
		if not self.email or "@" not in self.email:
			raise ValueError("Invalid email format")

		if self.status not in ("active", "inactive"):
			raise ValueError("Status must be 'active' or 'inactive'")

		if self.metadata is None:
			self.metadata = {}

	def is_active(self) -> bool:
		"""Check if user is active"""
		return self.status == "active"

	def deactivate(self) -> None:
		"""Deactivate the user"""
		self.status = "inactive"
		self.updated_at = datetime.now()

	def activate(self) -> None:
		"""Activate the user"""
		self.status = "active"
		self.updated_at = datetime.now()

	def update_last_login(self) -> None:
		"""Update last login timestamp"""
		self.last_login = datetime.now()
