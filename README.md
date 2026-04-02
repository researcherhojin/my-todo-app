# My Todo App

미니멀 TodoList 웹 앱. 사용자에게 꼭 필요한 것만 보여줍니다.

## 기술 스택
- **Backend:** FastAPI + SQLite (aiosqlite)
- **Frontend:** HTML + Vanilla JS + Bootstrap 5 CDN
- **Template:** Jinja2
- **패키지 관리:** uv

## 실행 방법
```bash
uv sync
uv run uvicorn app.main:app --reload
```
브라우저에서 http://localhost:8000 접속

## 테스트
```bash
uv run pytest tests/
```

## 프로젝트 구조
```
my-todo-app/
├── app/
│   ├── main.py            # FastAPI 엔트리포인트
│   ├── database.py        # SQLite 연결 + CRUD
│   ├── models.py          # Pydantic 요청/응답 모델
│   ├── routers/
│   │   └── todos.py       # /api/todos REST API
│   ├── templates/
│   │   └── index.html     # 메인 페이지
│   └── static/
│       ├── css/style.css   # 커스텀 스타일
│       └── js/app.js       # 프론트엔드 로직
└── tests/
    └── test_todos.py       # API 테스트
```

## 구현된 기능
- 할 일 추가 (Enter 또는 버튼, 빈 입력 방지)
- 할 일 목록 조회 (빈 상태 디자인 포함)
- 할 일 완료/미완료 토글 (취소선 + 투명도)
- 할 일 삭제 (애니메이션 적용)
- 할 일 인라인 수정 (더블클릭 → Enter 저장 / Esc 취소)
