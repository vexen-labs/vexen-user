"""Delete user use case."""

from dataclasses import dataclass

from vexen_user.application.dto import BaseResponse
from vexen_user.domain.repository import IUserRepositoryPort


@dataclass
class DeleteUser:
	"""Delete a user"""

	repository: IUserRepositoryPort

	async def __call__(self, user_id: str) -> BaseResponse[None]:
		try:
			user = await self.repository.get_by_id(user_id)
			if not user:
				return BaseResponse.fail(f"User with id {user_id} not found")

			await self.repository.delete(user_id)

			return BaseResponse.ok(None, message="User deleted successfully")

		except Exception as e:
			return BaseResponse.fail(f"Error deleting user: {str(e)}")
