"""Pydantic models for request/response validation."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator


class TodoCreate(BaseModel):
    """Request model for creating a new todo."""

    title: str

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        """Validate that title is not empty or whitespace-only."""
        if not v.strip():
            raise ValueError("할 일 내용을 입력해주세요")
        return v.strip()


class TodoUpdate(BaseModel):
    """Request model for updating a todo."""

    title: Optional[str] = None
    completed: Optional[bool] = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: Optional[str]) -> Optional[str]:
        """Validate that title is not empty or whitespace-only when provided."""
        if v is not None and not v.strip():
            raise ValueError("할 일 내용을 입력해주세요")
        return v.strip() if v is not None else v


class TodoResponse(BaseModel):
    """Response model for a todo item."""

    id: int
    title: str
    completed: bool
    position: int
    created_at: str
