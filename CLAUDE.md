# CLAUDE.md

## Project Overview
미니멀 TodoList 웹 앱. UX/UI 최우선. 불필요한 요소 제거.

## Tech Stack
- Backend: FastAPI + SQLite (aiosqlite)
- Frontend: HTML + Vanilla JS + Bootstrap 5 CDN
- Template: Jinja2

## Build & Run
pip install -r requirements.txt
uvicorn app.main:app --reload

## Test
pytest tests/

## Code Rules
- 변수명/함수명은 의미를 명확히 드러내는 영어 사용
- API 경로는 RESTful: /api/todos, /api/todos/{id}
- Pydantic 모델로 모든 요청/응답 타입 정의
- 에러 처리: 400 (잘못된 입력), 404 (존재하지 않는 리소스), 500 (서버 에러)
- docstring 필수
- 커밋 메시지: feat: / fix: / docs: / refactor: / chore: + 한국어 설명

## Architecture
app/main.py → app/routers/todos.py → app/database.py
                                    → app/models.py

## Dependency Direction
models → database → routers → main
(역방향 참조 금지)

## UX Design Principles
- 한 화면에 하나의 목적만
- 빈 상태(empty state)를 반드시 디자인
- 로딩/성공/에러 피드백을 사용자에게 제공
- 터치 타겟 최소 44px
- 색상은 최대 3가지 (배경, 텍스트, 강조)
