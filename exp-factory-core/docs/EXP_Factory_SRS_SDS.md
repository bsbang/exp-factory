# EXP-Core Idea Factory - 개발 문서
## SRS (Software Requirements Specification) & SDS (Software Design Specification)
Version: 1.0 | Date: 2026-11-04 | Author: EXP-Core Workspace Team

---

# PART 1: SRS - 요구사항 명세서

## 1. 개요 (Introduction)

### 1.1 목적 (Purpose)
본 문서는 "아이디어 한 줄로 게임/앱/툴을 자동 생산하는 Zero-Touch 팩토리"를 구축하기 위한 요구사항과 설계를 정의한다.
사용자는 관리자(Manager) 역할만 수행하며, 기획/개발/검증/배포의 실무는 AI Agent가 수행한다.
PC 부재 시에도 모바일 환경(Meta AI App + GitHub App)에서 지시/확인/승인이 가능해야 한다.

### 1.2 프로젝트 범위 (Scope)
- **Input:** 자연어 아이디어 (예: "벽돌깨기 게임, 부스터 있는거")
- **Output:** 배포 가능한 결과물 (Web Playable Game, Executable Tool, App)
- **Factory가 지원하는 장르:**
  - Game Phase 1: 퍼즐, 아케이드 (Godot 4 2D / Phaser Web)
  - Game Phase 2: 액션, 레이싱 (Godot 4 3D)
  - Tool: 동영상 화질 개선/편집 (Python + PyQt + FFmpeg + Real-ESRGAN)
  - App: 자산관리 앱 (Flutter / React)

### 1.3 용어 정의
| 용어 | 정의 |
| :--- | :--- |
| SSOT | Single Source of Truth. 진실은 채팅이 아닌 /docs 파일과 Git Commit |
| Idea Factory | 아이디어 -> Repo 생성 -> 기획 -> 개발 -> 배포까지 자동화하는 파이프라인 |
| Control Tower | Meta AI. 사용자와 팩토리의 유일한 인터페이스 |
| Executor | GitHub Actions (무료 클라우드). 실제 빌드/검증 수행 |
| Phase/Sprint | 개발 단계. 하나의 Phase는 하나의 채팅 세션으로 격리 |

## 2. 전체 설명 (Overall Description)

### 2.1 제품 관점
```
[User - Mobile/PC] <-> [Meta AI - Control Tower] <-> [GitHub - Factory Engine]
                                           |
                                           +-> Repo Template Registry
                                           +-> GitHub Actions (Windows/Linux Runner)
                                           +-> GitHub Pages (모바일 검증용 Web 배포)
```

### 2.2 사용자 역할
- **Manager (User):** 아이디어 제시, 기획 리뷰/승인, Phase별 결과물 확인/승인, 피드백. 코드는 직접 작성하지 않음.
- **Planner Agent (AI):** SRS, SDS, UI/UX Mockup 생성
- **Dev Agent (AI):** Phase별 코드 작성 (Groq Llama 3.1 70B + Ollama Local)
- **Verifier Agent (System):** 빌드, 테스트, AC(Acceptance Criteria) 자동 검증

### 2.3 운영 환경 제약
- 비용: 월 0원 (Free Tier Only)
- 빌드 환경: GitHub Actions Public Repo (무제한) / Private Repo (월 2000분 무료)
- 모바일 지원 필수: Meta AI App + GitHub App 2개로 전체 운영 가능

## 3. 기능 요구사항 (Functional Requirements)

### FR-01: 아이디어 기반 프로젝트 자동 생성 (Scaffolding)
- **설명:** 자연어 아이디어 입력 시 장르 분류 후 GitHub Repo 자동 생성
- **입력:** "벽돌깨기 게임 만들고 싶어"
- **처리:**
  1. `classify(idea)` -> `puzzle-arcade`
  2. `exp-template-puzzle-arcade` 템플릿으로부터 `brick-breaker-booster` Repo 생성
  3. Issue 생성: `[Factory] Phase 0: Planning`
- **출력:** GitHub Repo URL

### FR-02: 자동 기획 (Planning) - SRS/SDS/UI Mockup
- **SRS 요구사항:**
  - User Story 형식 (US-001...)
  - Acceptance Criteria 명시 (AC-001... 검증 가능한 수치 포함, 예: 60FPS 유지)
  - `docs/01_SRS.md`로 저장
- **SDS 요구사항:**
  - 시스템 아키텍처, 모듈 구조, 데이터 플로우
  - `docs/02_SDS.md`로 저장
- **UI/UX 요구사항:**
  - Meta AI 이미지 생성으로 목업 생성
  - `docs/03_UI_UX_Mockup.md`에 이미지 포함
  - 모바일에서 바로 확인 가능해야 함
- **검증:** 기획 문서는 PR로 생성되어야 하며, Manager 승인 전까지 개발 진행 불가

### FR-03: 마일스톤 자동 분해
- **설명:** 승인된 SRS/SDS를 기반으로 Phase/Sprint 자동 생성
- **처리:** `docs/04_Milestones.md` 생성 및 GitHub Milestones/Projects로 동기화
- **예시:**
  - Phase 1: Core Loop (Player, Ball)
  - Phase 2: Booster System
  - Phase 3: Polish & Release

### FR-04: 자율 개발 루프 (Autonomous Dev Loop)
- **Trigger:** `approve:phase-N` 라벨 부착 시
- **처리:**
  1. `meta_ai_agent.py`가 해당 Phase만 구현 (Context Slicing: SRS + 해당 Phase Milestone + 관련 파일 3개만 입력, 10k 토큰 이하)
  2. 빌드 수행 (Godot Export / MSBuild / Python build)
  3. `verify.py`로 AC 자동 검증
  4. 성공 시: Web Build를 GitHub Pages에 배포 + Artifact 업로드 + PR 생성
  5. 실패 시: 3회까지 자동 재시도, 그 이상은 실패 보고 후 중단
- **출력:** 플레이 가능한 Web 링크 + 빌드 로그 + 데모 영상 (Tool의 경우)

### FR-05: 모바일 지시/확인/승인
- **지시:** Meta AI App에서 자연어/음성으로 지시 가능
- **확인:**
  - GitHub App Push 알림 수신
  - Web 빌드 링크로 모바일 브라우저에서 즉시 플레이/확인
  - 빌드 실패 시 로그 요약 Meta AI가 전달
- **승인:** 아래 3가지 중 1개로 승인
  - Meta AI에게 "Phase N 승인"
  - GitHub PR에 "LGTM" 코멘트
  - GitHub PR에 👍 이모지

### FR-06: 피드백 반영 및 기획 업데이트
- **설명:** 개발 중 피드백 발생 시 SRS/SDS 업데이트 후 해당 Phase 재시작 가능
- **처리:** `feedback:minor/major` 라벨 기반

### FR-07: 최종 배포 (Release)
- **게임:** itch.io / GitHub Pages / GitHub Release (exe)
- **툴/앱:** GitHub Release에 Installer 포함

## 4. 비기능 요구사항 (Non-Functional Requirements)

### NFR-01: 환각 방지 (Anti-Hallucination) - 최우선
- **SSOT 원칙:** AI는 채팅 히스토리를 믿지 않고 /docs 파일만 신뢰. AGENT.md에 강제
- **Context Slicing:** 한 번에 하나의 Phase, 10k 토큰 이하, 관련 파일 3개 이하만 제공
- **Auto-Verifier:** 모든 결과물은 `verify.py`와 빌드 로그로 검증. AI의 "완료" 주장은 신뢰하지 않음
- **대화 격리:** Phase마다 채팅 세션 리셋

### NFR-02: 비용 0원 (Zero Cost)
- LLM: Groq Free API (Llama 3.1 70B) + Ollama Local (8B) 조합. OpenAI/Claude 유료 API 사용 금지
- CI/CD: GitHub Actions Public Repo 무제한 활용
- 저장소/협업: GitHub Free
- 이미지: Meta AI 이미지 생성 + Stable Diffusion Local
- 배포: GitHub Pages / itch.io

### NFR-03: 모바일 친화성
- 별도 앱 개발 없이 Meta AI App + GitHub App 2개로 운영
- 모든 결과물은 모바일 브라우저에서 확인 가능 (Web Build 필수)

### NFR-04: 확장성
- 새로운 장르 추가 시 템플릿 레포 1개만 추가하면 팩토리에 자동 등록되는 구조
- `exp-template-*` 네이밍 컨벤션 준수

---

# PART 2: SDS - 설계 명세서

## 5. 시스템 아키텍처 (System Architecture)

### 5.1 전체 아키텍처

```
Layer 1: Interface Layer (Mobile/PC)
  - Meta AI Chat (Control Tower)
  - GitHub Mobile App

Layer 2: Factory Core (Orchestration)
  - factory-cli.py: Repo 생성, 장르 분류
  - meta_ai_agent.py: 기획/개발 Agent (Groq API)
  - AGENT.md, verify.py: 가드레일

Layer 3: Template Registry
  - exp-template-puzzle-arcade (Godot 4 2D)
  - exp-template-action-racing (Godot 4 3D)
  - exp-template-video-tool (Python)
  - exp-template-asset-app (Flutter)

Layer 4: Execution Layer (Free Cloud)
  - GitHub Actions Workflows
    - ai-planning.yml: SRS/SDS 생성
    - ai-factory.yml: Phase별 개발/빌드/배포
  - GitHub Pages: Web Playable 배포
  - GitHub Artifacts: 빌드 결과물 보관

Layer 5: Observability
  - GitHub Projects (Kanban)
  - GitHub Issues (SRS/Task)
  - Actions Logs
```

### 5.2 상태 머신 (State Machine)

```
[0. IDEA] -- 아이디어 입력
  -> [1. SCAFFOLDING] 자동: Repo 생성
  -> [2. PLANNING] 자동: SRS/SDS/Mockup PR 생성
  -> [3. REVIEW_PLAN] 수동: Manager 승인 대기 (Gate)
  -> [4. MILESTONE] 자동: Phase 분해, Projects 생성
  -> [5. DEV] 자동: Phase N 개발 + 빌드 + 검증
  -> [6. REVIEW_PHASE] 수동: Manager 승인 대기 (Gate) - Web 링크 확인
  -> [7. LOOP] -> 5번으로 (다음 Phase)
  -> [8. RELEASE] 자동: 최종 배포
```

Gate(수동 승인) 외 모든 단계는 자동.

## 6. 모듈 설계 (Module Design)

### 6.1 factory-cli.py (Scaffolding Module)
- **함수:** `classify_idea(idea_text) -> genre`
  - 구현: 간단한 키워드 매칭 + Llama 8B 분류 (무료)
  - 예: "벽돌, 공, 부스터" -> puzzle-arcade
- **함수:** `create_repo_from_template(template, project_name) -> repo_url`
  - GitHub API 사용 (PyGithub)
- **함수:** `create_planning_issue(repo, idea)`

### 6.2 meta_ai_agent.py (AI Worker)
- **입력 제한 (Context Slicing):**
  ```python
  def get_context(phase):
      srs = read("docs/01_SRS.md")
      milestone = parse(f"docs/04_Milestones.md#{phase}")
      relevant_files = find_relevant(phase, max=3) # 벡터 검색 없이 파일명 매칭으로 무료 구현
      return truncate(srs + milestone + relevant_files, 10000)
  ```
- **LLM 호출:**
  - Primary: Groq API (llama-3.1-70b-versatile) - 무료, 빠름
  - Fallback: Ollama Local (llama3.1:8b) - 완전 무료, 오프라인
- **출력:** 코드 파일 수정 (core/ 폴더만)

### 6.3 verify.py (Verifier)
- **게임:** `godot --check`, FPS 체크, 파일 존재 여부
- **툴:** `pytest`, `ffmpeg -version`, 기능별 단위 테스트
- **공통:** 변경 금지 구역(예: Phase 1에서 UI 건드림) 감지

### 6.4 Workflows (GitHub Actions)

#### `ai-factory.yml`
```yaml
on: issues labeled
jobs:
  dev:
    if: startsWith(label, 'approve:phase-')
    runs-on: ubuntu-latest # or windows-latest for Godot
    steps:
      - checkout
      - run: python scripts/meta_ai_agent.py --phase ${{ label }}
      - run: python scripts/verify.py --phase ${{ label }}
      - run: godot --export-release Web build/web
      - uses: peaceiris/actions-gh-pages@v3 # 모바일 확인용 배포
      - uses: actions/upload-artifact@v4 # 다운로드용
      - run: gh pr create --title "Phase X Complete"
```

## 7. 데이터 설계 (Data Design)

### 7.1 문서 포맷 (SSOT)
- `docs/01_SRS.md`: User Story + AC 테이블
- `docs/02_SDS.md`: 아키텍처 다이어그램(Mermaid) + 모듈 정의
- `docs/03_UI_UX_Mockup.md`: 이미지 링크 + 설명
- `docs/04_Milestones.md`: Phase 정의 + 체크리스트

### 7.2 라벨 시스템 (Mobile Approval)
| 라벨 | 의미 | 누가 붙임 |
| :--- | :--- | :--- |
| factory:planning | 기획 생성 중 | System |
| status:need-review | Manager 리뷰 필요 | System |
| approve:phase-N | Phase N 승인, 다음 Phase 시작 | Manager (via Meta AI) |
| feedback:minor | 가벼운 수정 | Manager |
| feedback:major | 기획 재검토 | Manager |
| build:failed | 빌드 실패 | System |

## 8. 인터페이스 설계

### 8.1 Manager <-> Factory 인터페이스
- **자연어 명령 예시:**
  - "벽돌깨기 게임 만들어줘, 부스터 있는거로" -> FR-01 트리거
  - "기획안 보여줘" -> docs/ 파일 요약 + 이미지 표시
  - "Phase 1 승인" -> approve 라벨 부착
  - "공 속도 20% 빠르게 해줘" -> feedback Issue 생성

### 8.2 모바일 확인 인터페이스
- **Web Playable Link:** `https://{user}.github.io/{project}/` - 모바일 브라우저에서 즉시 플레이
- **Demo Video:** `build/demo.mp4` - 30초 자동 녹화 영상

## 9. 구현 로드맵 (Implementation Roadmap)

### Phase 0: Factory Core 구축 (1주차) - 현재 단계
- [ ] Template Registry 생성: exp-template-puzzle-arcade (Godot 4 2D 최소 구조)
- [ ] factory-cli.py + AGENT.md + verify.py 샘플 생성
- [ ] ai-factory.yml 기본 버전

### Phase 1: 공장 검증 - 퍼즐/아케이드 1호기 (2주차)
- 목표: "벽돌깨기" 아이디어로 전체 루프 1회 완주
- 성공 기준: 모바일에서 아이디어 입력 -> Web 플레이 링크 확인 -> 승인까지 1시간 이내

### Phase 2: 확장 (3주차)
- exp-template-action-racing 추가
- Groq Free API 연동 고도화

### Phase 3: Tool/App 확장 (4주차)
- exp-template-video-tool, exp-template-asset-app 추가
- itch.io / GitHub Release 자동 배포

## 10. 리스크 및 대응

| 리스크 | 대응 |
| :--- | :--- |
| 긴 대화로 인한 환각 | SSOT + Context Slicing + AGENT.md + verify.py 4중 방어 |
| GitHub Actions 무료 시간 초과 | Public Repo 전략 + Web Build 위주 (빌드 시간 짧음) |
| Godot 빌드 실패 | Docker 이미지 캐싱, `godot --export`만 사용 (에디터 실행 안함) |
| 모바일에서 코드 리뷰 어려움 | Web Playable + Demo Video로 코드 없이 결과물로만 리뷰 |

---
# 부록: 첫 번째 프로젝트 제안

**프로젝트명:** brick-breaker-booster
**장르:** puzzle-arcade (Phase 1 검증용)
**SRS 요약:**
- US-001: 패들로 공을 튕겨 벽돌을 깬다
- US-002: 빨간 부스터 아이템 획득 시 공 속도 50% 증가 (5초)
- AC-001: Web 빌드 60FPS 유지, 모바일 크롬에서 터치 조작 가능
**검증 방법:** GitHub Pages 링크로 모바일에서 플레이
**예상 소요:** 기획 10분 + Phase 1 개발 20분 + 검증 5분 = 35분

이 문서를 기반으로 Factory 1.0 구축을 시작합니다.
