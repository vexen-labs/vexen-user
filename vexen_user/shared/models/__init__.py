"""
Shared database models for vexen-user.

This module re-exports all SQLAlchemy models from their original locations
for centralized import. This facilitates future migration management with
tools like Alembic.

Usage:
    from vexen_user.shared.models import Base, UserModel
"""

from vexen_user.infraestructure.output.persistence.sqlalchemy.models.user import (
	Base,
	UserModel,
)

__all__ = ["Base", "UserModel"]
