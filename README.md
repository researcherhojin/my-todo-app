# My Todo App

미니멀 TodoList 웹 앱.

## 기술 스택
- Backend: FastAPI + SQLite (aiosqlite)
- Frontend: HTML + Vanilla JS + Bootstrap 5 CDN
- Template: Jinja2

## 실행 방법
```bash
uv sync
uv run uvicorn app.main:app --reload
```

## 테스트
```bash
uv run pytest tests/
```
