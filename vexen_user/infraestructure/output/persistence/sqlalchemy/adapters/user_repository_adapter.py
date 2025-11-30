"""User repository adapter for session management."""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from vexen_user.domain.entity.user import User
from vexen_user.domain.repository import IUserRepositoryPort
from vexen_user.infraestructure.output.persistence.sqlalchemy.repositories.user_repository import (
	UserRepository,
)


class UserRepositoryAdapter(IUserRepositoryPort):
	"""Adapter that manages SQLAlchemy sessions for user repository"""

	def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
		self._session_factory = session_factory

	async def get_by_id(self, user_id: str) -> User | None:
		async with self._session_factory() as session:
			repository = UserRepository(session)
			result = await repository.get_by_id(user_id)
			await session.commit()
			return result

	async def get_by_email(self, email: str) -> User | None:
		async with self._session_factory() as session:
			repository = UserRepository(session)
			result = await repository.get_by_email(email)
			await session.commit()
			return result

	async def save(self, user: User) -> User:
		async with self._session_factory() as session:
			repository = UserRepository(session)
			result = await repository.save(user)
			await session.commit()
			return result

	async def delete(self, user_id: str) -> None:
		async with self._session_factory() as session:
			repository = UserRepository(session)
			await repository.delete(user_id)
			await session.commit()

	async def list_paginated(
		self,
		page: int,
		page_size: int,
		search: str | None = None,
		role: str | None = None,
		status: str | None = None,
	) -> tuple[list[User], int]:
		async with self._session_factory() as session:
			repository = UserRepository(session)
			result = await repository.list_paginated(page, page_size, search, role, status)
			await session.commit()
			return result

	async def get_stats(self) -> dict:
		async with self._session_factory() as session:
			repository = UserRepository(session)
			result = await repository.get_stats()
			await session.commit()
			return result
