"""User service that orchestrates use cases."""

from dataclasses import dataclass, field

from vexen_user.application.dto import CreateUserRequest, PatchUserRequest, UpdateUserRequest
from vexen_user.application.usecase.user import UserUseCaseFactory
from vexen_user.domain.repository import IUserRepositoryPort


@dataclass
class UserService:
	"""Service layer for user operations"""

	repository: IUserRepositoryPort
	usecases: UserUseCaseFactory = field(init=False)

	def __post_init__(self):
		"""Initialize use case factory"""
		self.usecases = UserUseCaseFactory(repository=self.repository)

	async def list(
		self,
		page: int = 1,
		page_size: int = 20,
		search: str | None = None,
		role: str | None = None,
		status: str | None = None,
	):
		"""List users with pagination and filters"""
		return await self.usecases.list_users(page, page_size, search, role, status)

	async def get(self, user_id: str):
		"""Get user by ID with expanded details"""
		return await self.usecases.get_user(user_id)

	async def create(self, data: CreateUserRequest):
		"""Create a new user"""
		return await self.usecases.create_user(data)

	async def update(self, user_id: str, data: UpdateUserRequest):
		"""Update user (PUT)"""
		return await self.usecases.update_user(user_id, data)

	async def patch(self, user_id: str, data: PatchUserRequest):
		"""Update user partially (PATCH) - same as update for now"""
		# Convert PatchUserRequest to UpdateUserRequest
		update_data = UpdateUserRequest(
			name=data.name,
			avatar=data.avatar,
			status=data.status,
			user_metadata=data.user_metadata,
		)
		return await self.usecases.update_user(user_id, update_data)

	async def remove(self, user_id: str):
		"""Delete user"""
		return await self.usecases.delete_user(user_id)

	async def stats(self):
		"""Get user statistics"""
		return await self.usecases.get_stats()
