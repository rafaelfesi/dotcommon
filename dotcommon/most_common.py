from github import GithubException
from collections import Counter

def most_common(
    github, atomizer, paths, *, repo_count=100, progress_reporter=(lambda repo: None)
):
    counter = Counter()
    dot_repos = github.search_repositories(query="topic:dotfiles")

    for repo in dot_repos[:repo_count]:
        progress_reporter(repo)
        for path in paths:
            try:
                text = repo.get_contents(path).decoded_content.decode("utf-8")
                counter.update(atomizer(text))
                break
            except GithubException:
                pass

    return counter