# My Todo App

미니멀 TodoList 웹 앱.

## 기술 스택
- Backend: FastAPI + SQLite (aiosqlite)
- Frontend: HTML + Vanilla JS + Bootstrap 5 CDN
- Template: Jinja2

## 실행 방법
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 테스트
```bash
pytest tests/
```
