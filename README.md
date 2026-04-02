# My Todo App

> FastAPI + SQLite 기반의 미니멀 할 일 관리 웹 앱

## 스크린샷

| 빈 상태 | 할 일 목록 | 완료 상태 |
|---|---|---|
| ![빈 상태](docs/screenshots/final-01-empty.png) | ![목록](docs/screenshots/final-03-multiple.png) | ![완료](docs/screenshots/final-04-completed.png) |

| 인라인 편집 | 삭제 | 새로고침 후 유지 |
|---|---|---|
| ![편집](docs/screenshots/final-05-edited.png) | ![삭제](docs/screenshots/final-06-deleted.png) | ![새로고침](docs/screenshots/final-08-after-refresh.png) |

## 주요 기능

- **할 일 추가** — Enter 키 또는 "추가" 버튼. 빈 입력 시 shake 애니메이션 + 빨간 테두리
- **목록 조회** — 페이지 로드 시 자동 조회. 빈 상태/로딩/에러 각각 처리
- **완료 토글** — 커스텀 원형 체크박스 클릭. Optimistic Update + 서버 실패 시 롤백
- **삭제** — hover 시 x 버튼 노출. fade-out 0.3s 애니메이션 후 DOM 제거
- **인라인 편집** — 더블클릭으로 편집 모드 진입. Enter 저장, Esc 취소, blur 저장

## 디자인 원칙

MUJI 스타일 — 꾸미지 않아서 아름다운 것.

- 색상 3가지만: `#FAFAFA`(배경), `#1A1A1A`(텍스트), `#2563EB`(강조)
- CSS-only transition/animation (JS 애니메이션 금지)
- gradient, 이모지, 외부 아이콘 라이브러리 사용 금지
- 모든 상태를 디자인: 빈 상태, 로딩, 에러, 성공

## 빠른 시작

```bash
git clone https://github.com/researcherhojin/my-todo-app.git
cd my-todo-app
make setup
make dev
# → http://localhost:8000 (포트 사용 중이면 자동으로 8001, 8002로 전환)
```

## Make 명령어

| 명령어 | 설명 |
|---|---|
| `make setup` | 의존성 설치 (`uv sync`) |
| `make dev` | 개발 서버 실행 (포트 자동 탐색: 8000 → 8001 → 8002) |
| `make test` | pytest 실행 (14개 테스트) |
| `make test-ci` | CI 환경 테스트 (`--tb=short`) |
| `make check` | 서버 헬스체크 (포트 자동 탐색) |
| `make clean` | DB 파일 및 `__pycache__` 정리 |
| `make find-port` | 사용 가능한 포트 출력 |
| `make help` | 전체 명령어 도움말 |

## API

### `GET /api/todos/`
전체 목록 조회. `position` 오름차순 정렬.

**응답**: `200` — `[{ id, title, completed, position, created_at }]`

### `POST /api/todos/`
할 일 추가. 제목 앞뒤 공백 자동 제거.

**요청**: `{ "title": "string" }`
**응답**: `201` — `{ id, title, completed, position, created_at }`
**에러**: `422` — 빈 제목 또는 공백만 있는 제목

### `PATCH /api/todos/{id}`
제목 수정 또는 완료 상태 토글. 두 필드 모두 선택적.

**요청**: `{ "title?": "string", "completed?": bool }`
**응답**: `200` — `{ id, title, completed, position, created_at }`
**에러**: `400` — 수정할 필드 없음 | `404` — 존재하지 않는 ID | `422` — 빈 제목

### `DELETE /api/todos/{id}`
할 일 삭제.

**응답**: `204` — No Content
**에러**: `404` — 존재하지 않는 ID

## 기술 스택

| 구분 | 기술 |
|---|---|
| Backend | FastAPI, Python 3.12+, aiosqlite |
| Frontend | HTML, Vanilla JS, Bootstrap 5 CDN |
| Template | Jinja2 |
| Database | SQLite (`todo.db`, 자동 생성) |
| Package Manager | uv |
| CI | GitHub Actions (pytest + API smoke test) |
| 스크린샷 검증 | Playwright |

## 프로젝트 구조

```
app/
├── main.py          # FastAPI 앱 + Jinja2 템플릿 + lifespan
├── database.py      # SQLite 연결 + CRUD (유일한 aiosqlite importer)
├── models.py        # Pydantic 요청/응답 모델 + 입력 검증
├── routers/
│   └── todos.py     # /api/todos REST 라우터
├── templates/
│   └── index.html   # SPA 메인 페이지
└── static/
    ├── css/style.css  # CSS 변수 기반 커스텀 스타일
    └── js/app.js      # fetch API + Optimistic UI + 인라인 편집
```

## 버전 히스토리

- **v0.1.0** — MVP: CRUD + 미니멀 UX + Playwright 통합 검증
- **v0.0.1** — Harness 세팅: 프로젝트 구조, CI, STRATEGY.md
