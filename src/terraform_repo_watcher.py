
import os
import json
from http import client
import watcher_logging as log

# Make sure a list of repos was specified
registry_repos = os.getenv("REGISTRY_REPOS")
if registry_repos is None:
  raise Exception("Missing registry repos")

# Try deserialize the repo list
try:
  registry_repos = json.loads(registry_repos)
except Exception as error:
  log.error(f"REGISTRY_REPOS: {registry_repos}")
  log.error(error)
  raise Exception("Failed to deserialize $REGISTRY_REPOS!")

registry_endpoint = os.getenv("REGISTRY_ENDPOINT", "registry.terraform.io")
registry_path = os.getenv("REGISTRY_PATH", "/v1/modules")

conn = client.HTTPConnection(registry_endpoint)

def get_repo_stats(repo_list:list=registry_repos):
  repo_stats = []
  for repo in repo_list:
    conn.request("GET", f"{registry_path}/{repo}")
    response = conn.getresponse()
    if response.status == 200:
      data = response.read()
      repo_data = json.loads(data)
      repo_record = {
        "id": repo_data["id"],
        "owner": repo_data["owner"],
        "namespace": repo_data["namespace"],
        "name": repo_data["name"],
        "version": repo_data["version"],
        "provider": repo_data["provider"],
        "provider_logo_url": repo_data["provider_logo_url"],
        "description": repo_data["description"],
        "source": repo_data["source"],
        "tag": repo_data["tag"],
        "published_at": repo_data["published_at"],
        "downloads": repo_data["downloads"],
        "verified": repo_data["verified"]
      }
      repo_stats.append(repo_record)
  return repo_stats













