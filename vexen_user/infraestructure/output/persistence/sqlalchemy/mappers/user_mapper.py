"""Mapper between User entity and UserModel."""

from vexen_user.domain.entity.user import User
from vexen_user.infraestructure.output.persistence.sqlalchemy.models.user import (
	UserModel,
)


class UserMapper:
	"""Maps between User entity and UserModel"""

	@staticmethod
	def to_entity(model: UserModel) -> User:
		"""Convert model to entity"""
		return User(
			id=model.id,
			email=model.email,
			name=model.name,
			avatar=model.avatar,
			status=model.status,
			created_at=model.created_at,
			updated_at=model.updated_at,
			last_login=model.last_login,
			user_metadata=model.user_metadata or {},
		)

	@staticmethod
	def to_model(entity: User) -> UserModel:
		"""Convert entity to model"""
		return UserModel(
			id=entity.id,
			email=entity.email,
			name=entity.name,
			avatar=entity.avatar,
			status=entity.status,
			created_at=entity.created_at,
			updated_at=entity.updated_at,
			last_login=entity.last_login,
			user_metadata=entity.user_metadata,
		)

	@staticmethod
	def update_model_from_entity(model: UserModel, entity: User) -> UserModel:
		"""Update existing model from entity"""
		model.email = entity.email
		model.name = entity.name
		model.avatar = entity.avatar
		model.status = entity.status
		model.updated_at = entity.updated_at
		model.last_login = entity.last_login
		model.user_metadata = entity.user_metadata
		return model
