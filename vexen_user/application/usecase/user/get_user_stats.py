"""Get user statistics use case."""

from dataclasses import dataclass

from vexen_user.application.dto import BaseResponse, UserStatsResponse
from vexen_user.domain.repository import IUserRepositoryPort


@dataclass
class GetUserStats:
	"""Get user statistics"""

	repository: IUserRepositoryPort

	async def __call__(self) -> BaseResponse[UserStatsResponse]:
		try:
			stats = await self.repository.get_stats()

			response = UserStatsResponse(
				total=stats.get("total", 0),
				active=stats.get("active", 0),
				inactive=stats.get("inactive", 0),
				new_this_month=stats.get("new_this_month", 0),
				recent_logins=stats.get("recent_logins", 0),
			)

			return BaseResponse.ok(response)

		except Exception as e:
			return BaseResponse.fail(f"Error getting stats: {str(e)}")
