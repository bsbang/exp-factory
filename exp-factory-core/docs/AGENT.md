# AGENT.md - EXP Factory AI 행동 강령 (SSOT)

## 절대 규칙 (Anti-Hallucination)
1. 너는 절대 채팅 히스토리를 믿지 않는다. 진실은 오직 /docs/*.md 파일과 git log 뿐이다.
2. 코드 수정 전, 반드시 docs/01_SRS.md, docs/02_SDS.md, docs/04_Milestones.md를 읽어라.
3. 모르면 지어내지 말고 `TODO: Need human feedback`으로 남기고 멈춰라.
4. 한 번에 하나의 Phase만 수행한다. 다른 Phase 코드를 건드리면 실패다.
5. 500줄 이상 한 번에 생성 금지. 200줄 단위로 커밋.
6. 코드 생성 후 반드시 scripts/verify.py를 실행해야 한다. 실패 시 3회까지만 재시도.

## 작업 원칙
- 입력 토큰은 10k 이하로 유지 (SRS + 해당 Phase 마일스톤 + 관련 파일 3개만)
- 변경 금지 구역: Phase 1에서 /src/ui 건드리면 안됨. docs/에 명시.
- 모든 결과물은 PR로 생성. main에 직접 push 금지.
