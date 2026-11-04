import os
import pathlib
import subprocess
import shutil
import requests
from github import Github

ROOT = pathlib.Path(__file__).resolve().parents[3]
TEMPLATES_DIR = ROOT / "packages" / "templates"

def run(cmd):
    print(f"$ {cmd}")
    subprocess.check_call(cmd, shell=True)

def publish():
    token = os.getenv("FACTORY_GH_TOKEN","").strip()
    if not token:
        print("FACTORY_GH_TOKEN not set")
        return
    g = Github(token)
    user = g.get_user()
    print(f"User: {user.login}")
    if not TEMPLATES_DIR.exists():
        print(f"TEMPLATES_DIR not found: {TEMPLATES_DIR}")
        return
    for tmpl_dir in TEMPLATES_DIR.iterdir():
        if not tmpl_dir.is_dir():
            continue
        genre = tmpl_dir.name
        repo_name = f"exp-template-{genre}"
        print(f"\n=== Processing {genre} -> {repo_name} ===")
        try:
            repo = g.get_repo(f"{user.login}/{repo_name}")
            print(f"Repo exists: {repo.html_url}")
        except Exception:
            print(f"Creating repo {repo_name}")
            repo = user.create_repo(repo_name, private=False, description=f"Template {genre} for exp-factory")
            print(f"Created: {repo.html_url}")
        
        try:
            r = requests.patch(f"https://api.github.com/repos/{user.login}/{repo_name}",
                headers={"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"},
                json={"is_template": True})
            print(f"Set template flag: {r.status_code}")
        except Exception as e:
            print(f"Template flag error: {e}")

        tmp = pathlib.Path(f"/tmp/{repo_name}")
        if tmp.exists():
            shutil.rmtree(tmp)
        run(f"git clone https://{token}@github.com/{user.login}/{repo_name}.git {tmp}")
        for item in tmp.iterdir():
            if item.name == ".git":
                continue
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
        run(f"cp -r {tmpl_dir}/. {tmp}/")
        run(f"cd {tmp} && git config user.name 'factory-bot' && git config user.email 'factory-bot@users.noreply.github.com'")
        run(f"cd {tmp} && git add .")
        run(f"cd {tmp} && git commit -m 'auto publish {genre} from factory' || echo 'no changes'")
        run(f"cd {tmp} && git push origin HEAD:main || git push origin HEAD:master || true")
        print(f"Done {repo_name}")

if __name__ == "__main__":
    publish()
