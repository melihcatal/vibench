import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import requests


GITHUB_API_BASE = "https://api.github.com"


def _headers() -> Dict[str, str]:
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _parse_datetime(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    normalized = value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized)
    except ValueError:
        return None


def _fetch_org_secrets(org: str) -> List[Dict[str, Any]]:
    url = f"{GITHUB_API_BASE}/orgs/{org}/actions/secrets"
    response = requests.get(url, headers=_headers(), timeout=30)
    response.raise_for_status()
    return response.json().get("secrets", [])


def _fetch_repo_secrets(owner: str, repo: str) -> List[Dict[str, Any]]:
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/actions/secrets"
    response = requests.get(url, headers=_headers(), timeout=30)
    response.raise_for_status()
    return response.json().get("secrets", [])


def summarize_secret_rotation(secrets: List[Dict[str, Any]]) -> Dict[str, Any]:
    now = datetime.now(timezone.utc)
    total = len(secrets)
    rotated = 0
    stale = 0
    unknown = 0
    details = []

    for secret in secrets:
        updated_at = _parse_datetime(secret.get("updated_at"))
        if updated_at is None:
            unknown += 1
            status = "unknown"
        else:
            age_days = (now - updated_at).days
            if age_days <= 90:
                rotated += 1
                status = "rotated"
            else:
                stale += 1
                status = "stale"
        details.append(
            {
                "name": secret.get("name"),
                "updated_at": secret.get("updated_at"),
                "status": status,
            }
        )

    return {
        "total_secrets": total,
        "rotated_within_90_days": rotated,
        "stale_over_90_days": stale,
        "unknown_rotation": unknown,
        "details": details,
    }


def get_rotation_summary(scope: str, identifier: str) -> Dict[str, Any]:
    if scope == "org":
        secrets = _fetch_org_secrets(identifier)
    elif scope == "repo":
        if "/" not in identifier:
            raise ValueError("repo scope requires 'owner/repo'")
        owner, repo = identifier.split("/", 1)
        secrets = _fetch_repo_secrets(owner, repo)
    else:
        raise ValueError("scope must be 'org' or 'repo'")
    return summarize_secret_rotation(secrets)


if __name__ == "__main__":
    import json
    import sys

    if len(sys.argv) != 3:
        raise SystemExit("usage: rotation_summary.py <org|repo> <identifier>")
    print(json.dumps(get_rotation_summary(sys.argv[1], sys.argv[2]), indent=2, sort_keys=True))
