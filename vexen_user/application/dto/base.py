"""Base DTOs and response structures."""

from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class BaseResponse(Generic[T]):
	"""
	Generic response wrapper.

	Attributes:
		success: Whether the operation was successful
		data: The response data (if successful)
		error: Error message (if failed)
		message: Optional message
	"""

	success: bool
	data: T | None = None
	error: str | None = None
	message: str | None = None

	@classmethod
	def ok(cls, data: T, message: str | None = None) -> "BaseResponse[T]":
		"""Create a successful response"""
		return cls(success=True, data=data, error=None, message=message)

	@classmethod
	def fail(cls, error: str) -> "BaseResponse[T]":
		"""Create a failed response"""
		return cls(success=False, data=None, error=error)


@dataclass
class PaginationResponse:
	"""Pagination metadata"""

	page: int
	page_size: int
	total_pages: int
	total_items: int
	has_next: bool
	has_prev: bool


@dataclass
class PaginatedResponse(Generic[T]):
	"""Paginated response with data and pagination info"""

	success: bool
	data: list[T]
	pagination: PaginationResponse
	error: str | None = None

	@classmethod
	def ok(cls, data: list[T], pagination: PaginationResponse) -> "PaginatedResponse[T]":
		"""Create successful paginated response"""
		return cls(success=True, data=data, pagination=pagination, error=None)

	@classmethod
	def fail(cls, error: str) -> "PaginatedResponse[T]":
		"""Create failed paginated response"""
		return cls(
			success=False,
			data=[],
			pagination=PaginationResponse(
				page=1, page_size=20, total_pages=0, total_items=0, has_next=False, has_prev=False
			),
			error=error,
		)
