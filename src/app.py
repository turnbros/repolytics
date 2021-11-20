import os
import time
import elastic_output
import github_repo_watcher
import terraform_repo_watcher
import watcher_logging as log


def collect_repo_stats():
  ###############
  ## Github Stat Collection
  #############
  try:
    log.info("Get Github repo stats...")
    github_repo_stats = github_repo_watcher.get_repo_stats()
    log.info("Store Github repo stats...")
    github_es_index = os.getenv("GITHUB_ES_INDEX", "github")
    for github_repo_stat in github_repo_stats:
      elastic_output.index_repo_stat("github_repo_stat", github_repo_stat, github_es_index)
  except Exception as error:
    log.error("Failed to collect Terraform repo stats")
    log.error(error)

  ###############
  ## Terraform Stat Collection
  #############
  try:
    log.info("Get Terraform repo stats...")
    terraform_repo_stats = terraform_repo_watcher.get_repo_stats()
    log.info("Store Terraform repo stats...")
    terraform_es_index = os.getenv("REGISTRY_ES_INDEX", "terraform")
    for terraform_repo_stat in terraform_repo_stats:
      elastic_output.index_repo_stat("terraform_repo_stat", terraform_repo_stat, terraform_es_index)
  except Exception as error:
    log.error("Failed to collect Terraform repo stats")
    log.error(error)


if __name__ == "__main__":
  while True:
    print(os.getenv("ES_PASSWORD"))
    collect_repo_stats()
    time.sleep(2.4)
