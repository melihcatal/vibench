import os
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional

import requests


GITHUB_API_BASE = "https://api.github.com"


@dataclass
class SecretRotationSummary:
    provider: str
    repository: str
    total_secrets: int
    rotated_secrets: int
    overdue_secrets: int
    details: List[Dict[str, Any]]


def _auth_headers(token: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def _github_get(url: str, token: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    response = requests.get(url, headers=_auth_headers(token), params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def summarize_secret_rotation(owner: str, repo: str, token: Optional[str] = None) -> Dict[str, Any]:
    token = token or os.environ["GITHUB_TOKEN"]
    repository = f"{owner}/{repo}"
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/dependabot/secrets"
    data = _github_get(url, token)
    secrets = data.get("secrets", [])

    rotated = 0
    overdue = 0
    details: List[Dict[str, Any]] = []

    for secret in secrets:
        created_at = secret.get("created_at")
        updated_at = secret.get("updated_at")
        visibility = secret.get("visibility")
        name = secret.get("name")
        state = "rotated" if updated_at and created_at and updated_at != created_at else "stale"
        if state == "rotated":
            rotated += 1
        else:
            overdue += 1
        details.append(
            {
                "name": name,
                "visibility": visibility,
                "created_at": created_at,
                "updated_at": updated_at,
                "state": state,
            }
        )

    summary = SecretRotationSummary(
        provider="GitHub",
        repository=repository,
        total_secrets=len(secrets),
        rotated_secrets=rotated,
        overdue_secrets=overdue,
        details=details,
    )
    return asdict(summary)


if __name__ == "__main__":
    owner = os.environ.get("GITHUB_OWNER", "")
    repo = os.environ.get("GITHUB_REPO", "")
    print(summarize_secret_rotation(owner, repo))
