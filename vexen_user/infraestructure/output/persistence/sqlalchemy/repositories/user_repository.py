"""SQLAlchemy User repository implementation."""

import uuid
from datetime import datetime, timedelta

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from vexen_user.domain.entity.user import User
from vexen_user.domain.repository.user_repository_port import IUserRepositoryPort
from vexen_user.infraestructure.output.persistence.sqlalchemy.mappers.user_mapper import UserMapper
from vexen_user.infraestructure.output.persistence.sqlalchemy.models.user import UserModel


class UserRepository(IUserRepositoryPort):
	"""SQLAlchemy 2.0 async implementation of user repository"""

	def __init__(self, session: AsyncSession):
		self.session = session

	async def get_by_id(self, user_id: str) -> User | None:
		"""Get user by ID"""
		# Convert string to UUID for querying
		try:
			uuid_id = uuid.UUID(user_id)
		except (ValueError, AttributeError):
			return None

		stmt = select(UserModel).where(UserModel.id == uuid_id)
		result = await self.session.execute(stmt)
		model = result.scalar_one_or_none()

		if model is None:
			return None

		return UserMapper.to_entity(model)

	async def get_by_email(self, email: str) -> User | None:
		"""Get user by email"""
		stmt = select(UserModel).where(UserModel.email == email)
		result = await self.session.execute(stmt)
		model = result.scalar_one_or_none()

		if model is None:
			return None

		return UserMapper.to_entity(model)

	async def save(self, user: User) -> User:
		"""Create or update user"""
		if user.id:
			# Update existing
			stmt = select(UserModel).where(UserModel.id == user.id)
			result = await self.session.execute(stmt)
			existing_model = result.scalar_one_or_none()

			if existing_model:
				model = UserMapper.update_model_from_entity(existing_model, user)
			else:
				model = UserMapper.to_model(user)
				self.session.add(model)
		else:
			# Create new - the model will auto-generate UUID v7
			model = UserMapper.to_model(user)
			self.session.add(model)

		await self.session.flush()
		await self.session.refresh(model)

		return UserMapper.to_entity(model)

	async def delete(self, user_id: str) -> None:
		"""Delete user"""
		# Convert string to UUID for querying
		try:
			uuid_id = uuid.UUID(user_id)
		except (ValueError, AttributeError):
			return

		stmt = select(UserModel).where(UserModel.id == uuid_id)
		result = await self.session.execute(stmt)
		model = result.scalar_one_or_none()

		if model:
			await self.session.delete(model)
			await self.session.flush()

	async def list_paginated(
		self,
		page: int,
		page_size: int,
		search: str | None = None,
		role: str | None = None,
		status: str | None = None,
	) -> tuple[list[User], int]:
		"""List users with pagination and filters"""
		offset = (page - 1) * page_size

		# Build query with filters
		stmt = select(UserModel)

		if search:
			stmt = stmt.where(
				or_(
					UserModel.name.ilike(f"%{search}%"),
					UserModel.email.ilike(f"%{search}%"),
				)
			)

		if role:
			stmt = stmt.where(UserModel.role_id == role)

		if status:
			stmt = stmt.where(UserModel.status == status)

		# Get total count
		count_stmt = select(func.count()).select_from(stmt.subquery())
		total_result = await self.session.execute(count_stmt)
		total = total_result.scalar_one()

		# Get paginated results
		stmt = stmt.offset(offset).limit(page_size).order_by(UserModel.created_at.desc())
		result = await self.session.execute(stmt)
		models = result.scalars().all()

		users = [UserMapper.to_entity(model) for model in models]
		return users, total

	async def get_stats(self) -> dict:
		"""Get user statistics"""
		# Total users
		total_stmt = select(func.count()).select_from(UserModel)
		total_result = await self.session.execute(total_stmt)
		total = total_result.scalar_one()

		# Active users
		active_stmt = (
			select(func.count()).select_from(UserModel).where(UserModel.status == "active")
		)
		active_result = await self.session.execute(active_stmt)
		active = active_result.scalar_one()

		# Inactive users
		inactive = total - active

		# New users this month
		now = datetime.now()
		first_day_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
		new_this_month_stmt = (
			select(func.count())
			.select_from(UserModel)
			.where(UserModel.created_at >= first_day_of_month)
		)
		new_this_month_result = await self.session.execute(new_this_month_stmt)
		new_this_month = new_this_month_result.scalar_one()

		# Recent logins (last 7 days)
		seven_days_ago = now - timedelta(days=7)
		recent_logins_stmt = (
			select(func.count())
			.select_from(UserModel)
			.where(UserModel.last_login >= seven_days_ago)
		)
		recent_logins_result = await self.session.execute(recent_logins_stmt)
		recent_logins = recent_logins_result.scalar_one()

		return {
			"total": total,
			"active": active,
			"inactive": inactive,
			"new_this_month": new_this_month,
			"recent_logins": recent_logins,
		}
