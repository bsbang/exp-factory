"""
Meta AI Dev Agent - Groq Free API version
SRS + Phase 기반으로 코드 생성
"""
import os
import glob

# Groq 사용 예시 (무료)
# pip install groq
# from groq import Groq
# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def read_context(phase: str):
    context = ""
    try:
        with open("docs/01_SRS.md", "r", encoding="utf-8") as f:
            context += f.read() + "\n"
    except: pass
    try:
        with open("docs/04_Milestones.md", "r", encoding="utf-8") as f:
            context += f.read() + "\n"
    except: pass
    # 관련 파일 3개만 (비용 절감)
    files = glob.glob("src/**/*.gd", recursive=True) + glob.glob("src/**/*.py", recursive=True)
    for fp in files[:3]:
        try:
            with open(fp, "r", encoding="utf-8") as f:
                context += f"\n--- {fp} ---\n" + f.read()[:2000]
        except: pass
    return context[:10000]  # 10k 제한

def generate_code(phase: str, idea: str):
    context = read_context(phase)
    prompt = f"""
    너는 {phase} 개발자다. 다른 Phase는 건드리지 마.
    SRS와 Milestone을 만족하는 코드만 작성해.
    
    Context:
    {context}
    
    Task: {phase} 구현
    """
    print(prompt)
    # TODO: Groq API 호출로 코드 생성
    # 여기서는 더미로 파일 생성
    os.makedirs(f"src/core", exist_ok=True)
    with open(f"src/core/{phase}_impl.py", "w", encoding="utf-8") as f:
        f.write(f"# Auto-generated for {phase}\nprint('Hello from {phase}')\n")
    return True

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--phase", required=True)
    p.add_argument("--idea", default="")
    args = p.parse_args()
    generate_code(args.phase, args.idea)
