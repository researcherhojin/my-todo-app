"""SQLite database connection and table initialization."""

from typing import Optional

import aiosqlite

DATABASE_PATH = "todo.db"


async def get_db():
    """Get a database connection."""
    db = await aiosqlite.connect(DATABASE_PATH)
    db.row_factory = aiosqlite.Row
    try:
        yield db
    finally:
        await db.close()


async def init_db():
    """Create tables if they don't exist."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT 0,
                position INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        await db.commit()


async def fetch_all_todos(db: aiosqlite.Connection) -> list[dict]:
    """Fetch all todos ordered by position then creation time."""
    cursor = await db.execute(
        "SELECT id, title, completed, position, created_at FROM todos ORDER BY position ASC, created_at DESC"
    )
    rows = await cursor.fetchall()
    return [dict(row) for row in rows]


async def fetch_todo_by_id(db: aiosqlite.Connection, todo_id: int) -> Optional[dict]:
    """Fetch a single todo by ID."""
    cursor = await db.execute(
        "SELECT id, title, completed, position, created_at FROM todos WHERE id = ?",
        (todo_id,),
    )
    row = await cursor.fetchone()
    return dict(row) if row else None


async def create_todo(db: aiosqlite.Connection, title: str) -> dict:
    """Create a new todo and return it."""
    cursor = await db.execute(
        "SELECT COALESCE(MAX(position), -1) + 1 FROM todos"
    )
    row = await cursor.fetchone()
    next_position = row[0]

    cursor = await db.execute(
        "INSERT INTO todos (title, position) VALUES (?, ?)",
        (title, next_position),
    )
    await db.commit()

    return await fetch_todo_by_id(db, cursor.lastrowid)


async def update_todo(
    db: aiosqlite.Connection,
    todo_id: int,
    title: Optional[str] = None,
    completed: Optional[bool] = None,
) -> Optional[dict]:
    """Update a todo's title and/or completed status. Returns None if not found."""
    existing = await fetch_todo_by_id(db, todo_id)
    if not existing:
        return None

    updates = []
    params = []
    if title is not None:
        updates.append("title = ?")
        params.append(title)
    if completed is not None:
        updates.append("completed = ?")
        params.append(completed)

    if updates:
        params.append(todo_id)
        await db.execute(
            f"UPDATE todos SET {', '.join(updates)} WHERE id = ?",
            params,
        )
        await db.commit()

    return await fetch_todo_by_id(db, todo_id)


async def delete_todo(db: aiosqlite.Connection, todo_id: int) -> bool:
    """Delete a todo. Returns True if deleted, False if not found."""
    existing = await fetch_todo_by_id(db, todo_id)
    if not existing:
        return False

    await db.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    await db.commit()
    return True
