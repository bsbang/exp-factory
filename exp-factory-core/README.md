# EXP Factory Core - 아이디어 팩토리 엔진

이 레포가 공장 자체입니다.

## 구조
- /docs: SRS/SDS/AGENT.md (SSOT)
- /scripts: factory-cli.py, meta_ai_agent.py (Groq Free), verify.py
- /.github/workflows: 자동 개발 루프

## 최초 설정 (1회, 2분)
1. 이 레포를 Public으로 생성
2. Settings > Secrets and variables > Actions > New repository secret
   - `FACTORY_GH_TOKEN`: GitHub PAT (repo 생성 권한) - 완전 자동화 원하면
   - `GROQ_API_KEY`: https://console.groq.com 에서 무료 발급
3. Template 레포 생성: `exp-template-puzzle-arcade` (별도 zip)

## 사용법 (모바일)
1. Meta AI 앱에서: "벽돌깨기 게임 만들어줘"
2. Actions > Create Product Repo > Run workflow > idea, product_name 입력
   -> 자동으로 새 게임 레포 생성됨
3. 새 게임 레포에서 Planning PR 확인 -> LGTM
4. approve:phase-1 라벨 붙이면 자동 개발 시작 -> Web 링크로 모바일에서 플레이 확인

비용: 0원
