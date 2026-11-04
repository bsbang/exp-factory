import os
from github import Github
token=os.getenv("FACTORY_GH_TOKEN","").strip()
idea=os.getenv("IDEA","test idea")
prod=os.getenv("PRODUCT_NAME","brick-breaker-booster")
g=Github(token)
user=g.get_user()
genre='puzzle-arcade'
tname=f'exp-template-{genre}'
print(f"Creating product {prod} from {tname} with idea: {idea}")
try:
    tmpl=g.get_repo(f'{user.login}/{tname}')
    new=user.create_repo_from_template(name=prod, template_repo=tmpl, private=False, description=idea)
    print(f"Created from template: {new.html_url}")
except Exception as e:
    print(f"Template create failed: {e}, fallback empty")
    new=user.create_repo(prod, private=False, description=idea)
    print(f"Created empty: {new.html_url}")
