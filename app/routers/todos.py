"""API router for todo operations."""

from fastapi import APIRouter

router = APIRouter(prefix="/api/todos", tags=["todos"])
