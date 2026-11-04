"""
Verifier - AC 자동 검증
"""
import sys
import os

def verify(phase: str):
    print(f"[Verify] Phase: {phase}")
    # 1. 빌드 파일 존재 체크
    if not os.path.exists("src"):
        print("FAIL: src not found")
        return False
    # 2. 금지 구역 체크 예시
    # if phase == "phase-1" and os.path.exists("src/ui/polish.py"):
    #     print("FAIL: Phase 1에서 UI 건드리면 안됨")
    #     return False
    # 3. Godot 프로젝트 체크
    if os.path.exists("project.godot"):
        print("Godot project detected - check export")
    print("VERIFIED")
    return True

if __name__ == "__main__":
    phase = sys.argv[2] if len(sys.argv) > 2 else "phase-1"
    ok = verify(phase)
    sys.exit(0 if ok else 1)
