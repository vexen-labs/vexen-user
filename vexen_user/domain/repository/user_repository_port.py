"""User repository port (interface)."""

from abc import ABC, abstractmethod

from vexen_user.domain.entity.user import User


class IUserRepositoryPort(ABC):
	"""Interface for User repository"""

	@abstractmethod
	async def get_by_id(self, user_id: str) -> User | None:
		"""Get user by ID"""
		pass

	@abstractmethod
	async def get_by_email(self, email: str) -> User | None:
		"""Get user by email"""
		pass

	@abstractmethod
	async def save(self, user: User) -> User:
		"""Create or update user"""
		pass

	@abstractmethod
	async def delete(self, user_id: str) -> None:
		"""Delete user"""
		pass

	@abstractmethod
	async def list_paginated(
		self,
		page: int,
		page_size: int,
		search: str | None = None,
		role: str | None = None,
		status: str | None = None,
	) -> tuple[list[User], int]:
		"""
		List users with pagination and filters.

		Returns:
			Tuple of (users, total_count)
		"""
		pass

	@abstractmethod
	async def get_stats(self) -> dict:
		"""
		Get user statistics.

		Returns:
			Dictionary with stats: total, active, inactive, by_role, etc.
		"""
		pass
