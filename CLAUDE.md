# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

@docs/STRATEGY.md

## Project
미니멀 TodoList 웹 앱. UX 최우선. MUJI 스타일의 절제된 디자인.
Python 3.12, uv, SQLite (aiosqlite), FastAPI, Vanilla JS, Bootstrap 5 CDN.
Linter: 없음 (소규모 프로젝트). CI: GitHub Actions (test + smoke).

## Commands
```
make setup       # uv sync
make dev         # 서버 (포트 자동 탐색: 8000→8001→8002)
make test        # pytest
make clean       # DB/캐시 정리
make check       # 헬스체크
make find-port   # 사용 가능한 포트 출력
```
단독 테스트: `uv run pytest tests/test_todos.py::test_name`

## Architecture
```
app/main.py → app/routers/todos.py → app/database.py
                                    → app/models.py
```
의존성 방향: models → database → routers → main (역방향 참조 금지)

**DB as sole integration point:**
- `app/database.py`만 aiosqlite를 import
- 다른 모듈은 `database.py`의 함수를 통해서만 DB 접근
- `get_db()`는 async generator → `Depends(get_db)`로 주입
- `row_factory = aiosqlite.Row` 설정됨
- 테스트는 `tmp_path`로 독립 DB 격리

**DB schema:** Single `todos` table — `id` (autoincrement PK), `title`, `completed` (bool), `position` (int, for ordering), `created_at` (timestamp). New todos get `position = MAX(position) + 1`.

**Frontend:** `app.js`가 `/api/todos/`와 fetch로 통신. SPA 방식 — 페이지 새로고침 금지. Optimistic UI updates with rollback on error.

## Code Rules
- RESTful API: `/api/todos`, `/api/todos/{id}`
- Pydantic 모델로 모든 요청/응답 타입 정의
- 에러: 400 (잘못된 입력), 404 (존재하지 않는 리소스), 422 (검증 실패)
- docstring: 모든 함수, 클래스에 필수
- 커밋 메시지: `feat:`/`fix:`/`docs:`/`test:`/`chore:` + 한국어 설명
- `innerHTML` 금지 (체크마크 등 정적 요소 제외) → `textContent` 사용

## UX Rules
- 색상: #FAFAFA(배경), #1A1A1A(텍스트), #2563EB(강조)
- 추가 허용: #E5E5E5(border), #DC2626(에러), #fff
- border-radius ≤ 8px
- box-shadow: `0 1px 3px rgba(0,0,0,0.08)` — 1단계만
- 이모지/gradient/외부 아이콘 라이브러리 금지 (HTML entity만: ✓는 `&#10003;`)
- 체크박스: div + CSS 커스텀 (네이티브 checkbox 금지)
- 빈 상태: 반드시 디자인 (opacity 0.35, 중앙 정렬)
- 로딩/에러 피드백: 반드시 구현
- transition/animation: CSS only (JS 애니메이션 금지)
- 여백: 아이템 padding ≥ 12px, 터치 타겟 ≥ 44px
- Bootstrap 기본 스타일을 커스텀 CSS로 덮어써서 "Bootstrap스러움" 제거

## Testing Rules
- `pyproject.toml`에 `asyncio_mode = "auto"` 설정됨
- 비동기 fixture: `@pytest_asyncio.fixture` (not `@pytest.fixture`)
- 테스트 함수에 `@pytest.mark.asyncio` 붙이지 않음 (auto 모드)
- 각 테스트: `tmp_path`로 독립 DB 사용
- 테스트 클라이언트: `httpx.AsyncClient` + `ASGITransport`
- 테스트 패턴:
```python
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

@pytest_asyncio.fixture(autouse=True)
async def setup_db(tmp_path):
    test_db_path = str(tmp_path / "test.db")
    db_module.DATABASE_PATH = test_db_path
    await init_db()
    yield
    if os.path.exists(test_db_path):
        os.remove(test_db_path)

@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

async def test_example(client):
    res = await client.get("/api/todos/")
    assert res.status_code == 200
```

## Security Rules
- SQL Injection: 파라미터 바인딩 `?` 사용 (f-string SQL 금지)
- XSS: `textContent` 사용 (`innerHTML` 금지, 정적 요소 제외)
- 입력 검증: Pydantic 모델에서 서버 측 검증

## Playwright 검증
- 구현 후 반드시 Playwright로 브라우저 캡처
- 스크린샷: `docs/screenshots/`에 저장
- PR 본문에 스크린샷 첨부
- 포트 자동 탐색: `make find-port`로 확인 후 접속

## Session Log
- 커밋 전에 `docs/SESSION_LOG.md`에 해당 세션 작업을 append
- 형식: `# 세션 — YYYY-MM-DD` 헤더 + 타임라인/문제/커밋/교훈
- 이전 세션 내용은 수정하지 않는다 (append only)
- 상세 규칙: `docs/AGENT_PROMPT.md` §0.5 참조
