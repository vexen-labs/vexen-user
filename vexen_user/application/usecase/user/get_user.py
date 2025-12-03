"""Get user by ID use case."""

from dataclasses import dataclass

from vexen_user.application.dto import BaseResponse, UserExpandedResponse
from vexen_user.domain.repository import IUserRepositoryPort


@dataclass
class GetUser:
	"""Get user by ID with expanded details"""

	repository: IUserRepositoryPort

	async def __call__(self, user_id: str) -> BaseResponse[UserExpandedResponse]:
		try:
			user = await self.repository.get_by_id(user_id)

			if not user:
				return BaseResponse.fail(f"User with id {user_id} not found")

			response = UserExpandedResponse(
				id=user.id,
				email=user.email,
				name=user.name,
				avatar=user.avatar,
				status=user.status,
				created_at=user.created_at,
				updated_at=user.updated_at,
				last_login=user.last_login,
				user_metadata=user.user_metadata or {},
			)

			return BaseResponse.ok(response)

		except Exception as e:
			return BaseResponse.fail(f"Error getting user: {str(e)}")
