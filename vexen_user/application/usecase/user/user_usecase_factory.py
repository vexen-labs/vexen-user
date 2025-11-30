"""Factory for user use cases."""

from dataclasses import dataclass, field

from vexen_user.domain.repository import IUserRepositoryPort

from .create_user import CreateUser
from .delete_user import DeleteUser
from .get_user import GetUser
from .get_user_stats import GetUserStats
from .list_users import ListUsers
from .update_user import UpdateUser


@dataclass
class UserUseCaseFactory:
	"""Factory for creating user use cases"""

	repository: IUserRepositoryPort

	list_users: ListUsers = field(init=False)
	get_user: GetUser = field(init=False)
	create_user: CreateUser = field(init=False)
	update_user: UpdateUser = field(init=False)
	delete_user: DeleteUser = field(init=False)
	get_stats: GetUserStats = field(init=False)

	def __post_init__(self):
		"""Initialize all use cases"""
		self.list_users = ListUsers(repository=self.repository)
		self.get_user = GetUser(repository=self.repository)
		self.create_user = CreateUser(repository=self.repository)
		self.update_user = UpdateUser(repository=self.repository)
		self.delete_user = DeleteUser(repository=self.repository)
		self.get_stats = GetUserStats(repository=self.repository)
