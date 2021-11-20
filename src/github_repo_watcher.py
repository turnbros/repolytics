import os
import json
from github import Github
import watcher_logging as log

# Make sure the Github token was specified
access_token = os.getenv("GITHUB_TOKEN")
if access_token is None:
  raise Exception("Missing Github access token!")

# Make sure a list of Github repos was specified
github_repos = os.getenv("GITHUB_REPOS")
if github_repos is None:
  raise Exception("Missing Github repos")

# Try deserialize the repo list
try:
  github_repos = json.loads(github_repos)
except Exception as error:
  log.error(f"GITHUB_REPOS: {github_repos}")
  log.error(error)
  raise Exception("Failed to deserialize $GITHUB_REPOS!")

g = Github(access_token)

def get_repo_stats(repo_list:list=github_repos) -> list:
  repo_stats = []
  for repo_name in repo_list:
    repo = g.get_repo(repo_name)
    
    repo_open_issues = repo.get_issues(state='open')
    repo_stars = repo.stargazers_count
    repo_forks = repo.forks
    repo_top_referrers = repo.get_top_referrers()
    repo_top_paths = repo.get_top_paths()
    repo_clone_traffic = repo.get_clones_traffic()
    repo_view_traffic = repo.get_views_traffic()
    
    repo_stats_top_referrers = []
    for top_referrer in repo_top_referrers:
      repo_stats_top_referrers.append({
        "referrer": top_referrer.referrer,
        "count": top_referrer.count,
        "uniques": top_referrer.uniques
      })

    repo_stats_top_paths = []
    for top_path in repo_top_paths:
      repo_stats_top_paths.append({
        "path": top_path.path,
        "title": top_path.title,
        "uniques": top_path.uniques,
        "count": top_path.count
      })

    repo_stats.append({
      "repo_name": repo_name,
      "open_issues": repo_open_issues.totalCount,
      "forks": repo_forks,
      "stars": repo_stars,
      "top_paths": repo_stats_top_paths,
      "top_referrers": repo_stats_top_referrers,
      "traffic_unique_clones": repo_clone_traffic.get("uniques"),
      "traffic_total_clones": repo_clone_traffic.get("count"),
      "traffic_unique_views": repo_view_traffic.get("uniques"),
      "traffic_total_views": repo_view_traffic.get("count")
    })

  return repo_stats