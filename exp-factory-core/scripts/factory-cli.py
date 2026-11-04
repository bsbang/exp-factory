"""
Factory CLI - 아이디어 -> 장르 분류 -> Repo 생성
GitHub Actions에서 실행됨. 로컬에서도 실행 가능.
"""
import os
import sys
from github import Github

GENRE_KEYWORDS = {
    "puzzle-arcade": ["퍼즐", "벽돌", "2048", "테트리스", "브레이크", "아케이드", "puzzle", "brick", "arcade", "flappy"],
    "action-racing": ["액션", "레이싱", "슈팅", "action", "racing", "shooter", "survivor"],
    "video-tool": ["동영상", "화질", "편집", "업스케일", "video", "upscale", "edit"],
    "asset-app": ["자산", "가계부", "관리", "앱", "asset", "finance", "todo"]
}

def classify_idea(idea: str) -> str:
    idea_low = idea.lower()
    for genre, keywords in GENRE_KEYWORDS.items():
        for kw in keywords:
            if kw in idea_low:
                return genre
    return "puzzle-arcade"  # default

def create_product_repo(product_name: str, template_repo_name: str, idea: str):
    token = os.getenv("FACTORY_GH_TOKEN") or os.getenv("GITHUB_TOKEN")
    if not token:
        print("No token found. Manual mode.")
        return None
    g = Github(token)
    user = g.get_user()
    # 템플릿 찾기
    try:
        template_repo = g.get_repo(f"{user.login}/{template_repo_name}")
    except Exception as e:
        print(f"Template repo not found: {template_repo_name} {e}")
        # fallback to create empty repo
        new_repo = user.create_repo(product_name, private=False, description=f"Auto-generated: {idea}")
        return new_repo.html_url

    new_repo = user.create_repo_from_template(
        name=product_name,
        template_repo=template_repo,
        private=False,
        description=f"Factory product: {idea}"
    )
    # 초기 이슈 생성
    new_repo.create_issue(
        title=f"[Factory] Phase 0: Planning for {idea}",
        body=f"IDEA: {idea}\n\nGENRE: {classify_idea(idea)}\n\n@factory-bot docs/ 를 생성해줘. SRS/SDS/UI Mockup 포함.",
        labels=["factory:planning", "status:need-review"]
    )
    print(f"Created: {new_repo.html_url}")
    return new_repo.html_url

if __name__ == "__main__":
    idea = sys.argv[1] if len(sys.argv) > 1 else "벽돌깨기 게임"
    genre = classify_idea(idea)
    print(f"Idea: {idea} -> Genre: {genre}")
    # 예: python factory-cli.py "벽돌깨기 게임" --name brick-breaker-booster
