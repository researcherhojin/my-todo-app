"""API router for todo operations."""

from fastapi import APIRouter, Depends, HTTPException, status
from aiosqlite import Connection

from app.database import get_db, fetch_all_todos, create_todo, fetch_todo_by_id, update_todo, delete_todo
from app.models import TodoCreate, TodoUpdate, TodoResponse

router = APIRouter(prefix="/api/todos", tags=["todos"])


@router.get("/", response_model=list[TodoResponse])
async def list_todos(db: Connection = Depends(get_db)):
    """Fetch all todos."""
    todos = await fetch_all_todos(db)
    return todos


@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def add_todo(todo: TodoCreate, db: Connection = Depends(get_db)):
    """Create a new todo item."""
    new_todo = await create_todo(db, todo.title)
    return new_todo


@router.patch("/{todo_id}", response_model=TodoResponse)
async def modify_todo(todo_id: int, todo: TodoUpdate, db: Connection = Depends(get_db)):
    """Update a todo's title or completed status."""
    if todo.title is None and todo.completed is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="수정할 내용을 입력해주세요",
        )

    updated = await update_todo(db, todo_id, title=todo.title, completed=todo.completed)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="할 일을 찾을 수 없습니다",
        )
    return updated


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_todo(todo_id: int, db: Connection = Depends(get_db)):
    """Delete a todo item."""
    deleted = await delete_todo(db, todo_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="할 일을 찾을 수 없습니다",
        )
