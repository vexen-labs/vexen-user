"""List users use case."""

from dataclasses import dataclass

from vexen_user.application.dto import (
	PaginatedResponse,
	PaginationResponse,
	UserResponse,
)
from vexen_user.domain.repository import IUserRepositoryPort


@dataclass
class ListUsers:
	"""List users with pagination and filters"""

	repository: IUserRepositoryPort

	async def __call__(
		self,
		page: int = 1,
		page_size: int = 20,
		search: str | None = None,
		role: str | None = None,
		status: str | None = None,
	) -> PaginatedResponse[UserResponse]:
		try:
			users, total = await self.repository.list_paginated(
				page, page_size, search, role, status
			)

			response_data = [
				UserResponse(
					id=u.id,
					email=u.email,
					name=u.name,
					avatar=u.avatar,
					status=u.status,
					created_at=u.created_at,
					last_login=u.last_login,
				)
				for u in users
			]

			total_pages = (total + page_size - 1) // page_size
			pagination = PaginationResponse(
				page=page,
				page_size=page_size,
				total_pages=total_pages,
				total_items=total,
				has_next=page < total_pages,
				has_prev=page > 1,
			)

			return PaginatedResponse.ok(response_data, pagination)

		except Exception as e:
			return PaginatedResponse.fail(f"Error listing users: {str(e)}")
