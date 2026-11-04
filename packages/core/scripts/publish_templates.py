
import os, pathlib, subprocess
from github import Github
ROOT = pathlib.Path(__file__).resolve().parents[3]
TEMPLATES_DIR = ROOT / "packages" / "templates"
def run(cmd):
    print(f"$ {cmd}")
    subprocess.check_call(cmd, shell=True)
def publish():
    token = os.getenv("FACTORY_GH_TOKEN")
    if not token: return
    g = Github(token)
    user = g.get_user()
    for tmpl_dir in TEMPLATES_DIR.iterdir():
        if not tmpl_dir.is_dir(): continue
        genre = tmpl_dir.name
        repo_name = f"exp-template-{genre}"
        try:
            repo = g.get_repo(f"{user.login}/{repo_name}")
        except:
            repo = user.create_repo(repo_name, private=False, description=f"Template {genre}", is_template=True)
        import requests, time
        requests.patch(f"https://api.github.com/repos/{user.login}/{repo_name}", headers={"Authorization": f"token {token}"}, json={"is_template": True})
        tmp = pathlib.Path(f"/tmp/{repo_name}")
        if tmp.exists(): run(f"rm -rf {tmp}")
        run(f"git clone https://{token}@github.com/{user.login}/{repo_name}.git {tmp}")
        run(f"find {tmp} -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {{}} +")
        run(f"cp -r {tmpl_dir}/. {tmp}/")
        run(f"cd {tmp} && git config user.name 'factory-bot' && git config user.email 'factory-bot@users.noreply.github.com'")
        run(f"cd {tmp} && git add . && git commit -m 'auto publish {genre}' || true")
        run(f"cd {tmp} && git push origin main || git push origin master || true")
if __name__ == "__main__":
    publish()
