"""
VexenUser - Public API for the vexen-user library.

This module provides the main entry point for using the vexen-user system.
"""

from dataclasses import dataclass
from typing import Literal

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from vexen_user.application.service.user_service import UserService
from vexen_user.domain.repository import IUserRepositoryPort
from vexen_user.infraestructure.output.persistence.sqlalchemy.adapters import (
	user_repository_adapter,
)
from vexen_user.infraestructure.output.persistence.sqlalchemy.models.user import Base


@dataclass
class VexenUserConfig:
	"""Configuration for VexenUser"""

	database_url: str
	adapter: Literal["sqlalchemy"] = "sqlalchemy"
	echo: bool = False
	pool_size: int = 5
	max_overflow: int = 10


class VexenUser:
	"""
	Main entry point for vexen-user system.

	Example:
		```python
		from vexen_user import VexenUser

		# Initialize
		user_system = VexenUser(
			database_url="postgresql+asyncpg://user:pass@localhost/db"
		)

		await user_system.init()

		# Use the service
		users = await user_system.service.list(page=1, page_size=20)

		# Clean up
		await user_system.close()
		```
	"""

	def __init__(
		self,
		database_url: str | None = None,
		adapter: Literal["sqlalchemy"] = "sqlalchemy",
		echo: bool = False,
		pool_size: int = 5,
		max_overflow: int = 10,
	):
		"""
		Initialize VexenUser.

		Args:
			database_url: Database connection string
			adapter: Repository adapter to use (currently only 'sqlalchemy')
			echo: Enable SQL echo (for debugging)
			pool_size: Connection pool size
			max_overflow: Max overflow connections
		"""
		self.config = VexenUserConfig(
			database_url=database_url or "",
			adapter=adapter,
			echo=echo,
			pool_size=pool_size,
			max_overflow=max_overflow,
		)

		self._engine = None
		self._session_factory = None
		self._repository: IUserRepositoryPort | None = None
		self._service: UserService | None = None

	async def init(self) -> None:
		"""
		Initialize the user system.

		This creates the database engine, session factory, and initializes repositories.
		"""
		if self.config.adapter == "sqlalchemy":
			await self._init_sqlalchemy()
		else:
			raise ValueError(f"Unsupported adapter: {self.config.adapter}")

		# Initialize service
		self._service = UserService(repository=self._repository)

	async def _init_sqlalchemy(self) -> None:
		"""Initialize SQLAlchemy engine and repositories"""
		self._engine = create_async_engine(
			self.config.database_url,
			echo=self.config.echo,
			pool_size=self.config.pool_size,
			max_overflow=self.config.max_overflow,
		)

		self._session_factory = async_sessionmaker(
			self._engine, class_=AsyncSession, expire_on_commit=False
		)

		# Create tables
		async with self._engine.begin() as conn:
			await conn.run_sync(Base.metadata.create_all)

		# Initialize repositories
		self._repository = user_repository_adapter.UserRepositoryAdapter(
			self._session_factory
		)

	async def close(self) -> None:
		"""Close database connections and clean up resources"""
		if self._engine:
			await self._engine.dispose()

	@property
	def service(self) -> UserService:
		"""
		Get the user service.

		Returns:
			UserService: Service for user operations

		Raises:
			RuntimeError: If init() hasn't been called
		"""
		if self._service is None:
			raise RuntimeError("VexenUser not initialized. Call await vexen_user.init() first")
		return self._service

	@property
	def repository(self) -> IUserRepositoryPort:
		"""
		Get the user repository (for advanced use).

		Returns:
			IUserRepositoryPort: User repository

		Raises:
			RuntimeError: If init() hasn't been called
		"""
		if self._repository is None:
			raise RuntimeError("VexenUser not initialized. Call await vexen_user.init() first")
		return self._repository

	# Context manager support
	async def __aenter__(self):
		"""Async context manager entry"""
		await self.init()
		return self

	async def __aexit__(self, exc_type, exc_val, exc_tb):
		"""Async context manager exit"""
		await self.close()
