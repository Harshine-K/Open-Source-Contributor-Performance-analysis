import pandas as pd
import requests
import json

GITHUB_API_URL = "https://api.github.com"
TOKEN = "API_KEY"  # Replace with your GitHub API token

HEADERS = {"Authorization": f"token {TOKEN}"}

# Fetch contributor data
def get_contributors(owner, repo):
    contributors = []
    page = 1
    while True:
        url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/contributors?page={page}&per_page=100"
        response = requests.get(url, headers=HEADERS)

        if response.status_code == 200:
            data = response.json()
            if not data:
                break
            contributors.extend(data)
            page += 1
        else:
            print(f"Failed to fetch contributors: {response.status_code}")
            return None
    return contributors

# Fetch commits
def get_commits(owner, contributions, repo):
    for i in contributions:
        login = i['login']
        page = 1
        while True:
            url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/commits?author={login}&page={page}&per_page=100"
            response = requests.get(url, headers=HEADERS)

            if response.status_code == 200:
                commits = response.json()
                if not commits:
                    break
                i['commits'] += len(commits)
                page += 1
            else:
                print(f"Failed to fetch commits for {login}: {response.status_code}")
                break
    print("Commits updated")
    return contributions

# Fetch pull requests
def get_pull_requests(owner, df, repo):
    page = 1
    new_rows = []
    while True:
        url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls?state=all&page={page}&per_page=100"
        response = requests.get(url, headers=HEADERS)

        if response.status_code == 200:
            prs = response.json()
            if not prs:
                break
            for pr in prs:
                user = pr['user']['login']
                if user in df['login'].values:
                    df.loc[df['login'] == user, 'pull_requests'] += 1
                else:
                    new_rows.append({'login': user, 'id': pr['user']['login'], 'url': pr['user']['html_url'], 'contributions': None, 'commits': 0, 'pull_requests': 1, 'issues': 0})
            page += 1
        else:
            print(f"Failed to fetch pull requests: {response.status_code}")
            return None
    if new_rows:
        new_df = pd.DataFrame(new_rows)
        df = pd.concat([df, new_df], ignore_index=True)
    print("Pull requests updated")
    return df

# Fetch issues
def get_issues(owner, df, repo):
    page = 1
    new_rows = []
    while True:
        url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/issues?page={page}&per_page=100"
        response = requests.get(url, headers=HEADERS)

        if response.status_code == 200:
            issues = response.json()
            if not issues:
                break
            for issue in issues:
                reporter = issue['user']['login']
                if reporter in df['login'].values:
                    df.loc[df['login'] == reporter, 'issues'] += 1
                else:
                    new_rows.append({'login': reporter, 'id': issue['user']['id'], 'url': issue['user']['html_url'], 'contributions': None, 'commits': 0, 'pull_requests': 0, 'issues': 1})
            page += 1
        else:
            print(f"Failed to fetch issues: {response.status_code}")
            return None
    if new_rows:
        new_df = pd.DataFrame(new_rows)
        df = pd.concat([df, new_df], ignore_index=True)
    print("Issues updated")
    return df

# Main script execution
def main():
    owner = "facebook"  # Change to your desired repository owner
    repo = "react"  # Change to your desired repository name

    contributors = get_contributors(owner, repo)
    contributions = []
    for i in contributors:
        l = {'login': i['login'], 'id': i['id'], 'url': i['html_url'], 'contributions': i['contributions'], 'commits': 0, 'pull_requests': 0, 'issues': 0}
        contributions.append(l)

    contributions = get_commits(owner, contributions, repo)
    contributions_df = pd.DataFrame(contributions)
    contributions_df = get_pull_requests(owner, contributions_df, repo)
    contributions_df = get_issues(owner, contributions_df, repo)

    contributions_df.to_csv('contributors.csv', index=False)
    print("Contributor data saved to contributors.csv")

if __name__ == "__main__":
    main()