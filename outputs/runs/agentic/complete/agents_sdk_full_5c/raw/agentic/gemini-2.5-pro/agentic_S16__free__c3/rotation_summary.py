import requests
from security_client import get_github_token
from security_models import SecretRotationInfo

def get_rotation_summary(repo: str, secret_label: str = "secret-rotation") -> list[SecretRotationInfo]:
    """
    Summarizes secret rotation status by searching for issues on GitHub.

    Args:
        repo: The owner/repository string (e.g., "myorg/myrepo").
        secret_label: The label used to tag issues related to secret rotation.

    Returns:
        A list of SecretRotationInfo objects.
    """
    token = get_github_token()
    if not token:
        print("GitHub token not found. Please set GITHUB_TOKEN environment variable.")
        return []

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    url = f"https://api.github.com/repos/{repo}/issues"
    params = {"labels": secret_label, "state": "all"}

    summaries = []
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        issues = response.json()

        for issue in issues:
            status = "pending"
            if issue.get("state") == "closed":
                status = "completed"
            
            # Simplified logic: use issue dates as proxies for rotation dates
            summary = SecretRotationInfo(
                secret_name=issue.get("title", "Unknown Secret"),
                last_rotated=issue.get("closed_at"),
                next_rotation=issue.get("created_at"), # Simplified for demo
                status=status
            )
            summaries.append(summary)
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from GitHub API: {e}")

    return summaries

# Example usage would be in a different file.
# if __name__ == "__main__":
#     github_repo = "your_org/your_repo" # Replace with a real repo
#     rotation_summaries = get_rotation_summary(github_repo)
    
#     if rotation_summaries:
#         print(f"Found {len(rotation_summaries)} secret rotation tasks in {github_repo}:")
#         for summary in rotation_summaries:
#             print(f"- {summary.secret_name}: Status is {summary.status}")
#     else:
#         print("No rotation summaries found or an error occurred.")
