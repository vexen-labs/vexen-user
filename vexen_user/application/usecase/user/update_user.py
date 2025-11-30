"""Update user use case."""

from dataclasses import dataclass
from datetime import datetime

from vexen_user.application.dto import (
	BaseResponse,
	UpdateUserRequest,
	UserResponse,
)
from vexen_user.domain.repository import IUserRepositoryPort


@dataclass
class UpdateUser:
	"""Update user (PUT - replaces all fields)"""

	repository: IUserRepositoryPort

	async def __call__(
		self, user_id: str, data: UpdateUserRequest
	) -> BaseResponse[UserResponse]:
		try:
			user = await self.repository.get_by_id(user_id)
			if not user:
				return BaseResponse.fail(f"User with id {user_id} not found")

			# Update fields
			if data.name is not None:
				user.name = data.name
			if data.avatar is not None:
				user.avatar = data.avatar
			if data.status is not None:
				user.status = data.status
			if data.metadata is not None:
				user.metadata = data.metadata

			user.updated_at = datetime.now()

			# Save
			updated_user = await self.repository.save(user)

			response = UserResponse(
				id=updated_user.id,
				email=updated_user.email,
				name=updated_user.name,
				avatar=updated_user.avatar,
				status=updated_user.status,
				created_at=updated_user.created_at,
				last_login=updated_user.last_login,
			)

			return BaseResponse.ok(response)

		except Exception as e:
			return BaseResponse.fail(f"Error updating user: {str(e)}")
