import os
from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional

import requests


GITHUB_API_BASE = "https://api.github.com"
GITHUB_TOKEN_ENV = "GITHUB_TOKEN"


def _headers() -> Dict[str, str]:
    headers = {"Accept": "application/vnd.github+json"}
    token = os.getenv(GITHUB_TOKEN_ENV)
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _iso_to_dt(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value)


def _fetch_repo_events(owner: str, repo: str, per_page: int = 100) -> List[Dict[str, Any]]:
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/events"
    response = requests.get(url, headers=_headers(), params={"per_page": per_page}, timeout=30)
    response.raise_for_status()
    return response.json()


def _summarize_events(events: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    usage_by_actor = Counter()
    event_counts = Counter()
    crypto_events = []
    latest_seen: Optional[datetime] = None

    crypto_types = {
        "PushEvent",
        "CreateEvent",
        "DeleteEvent",
        "ReleaseEvent",
        "PublicEvent",
        "ForkEvent",
        "WatchEvent",
        "PullRequestEvent",
        "PullRequestReviewEvent",
        "IssueCommentEvent",
    }

    for event in events:
        event_type = event.get("type", "unknown")
        actor = (event.get("actor") or {}).get("login") or "unknown"
        event_counts[event_type] += 1
        usage_by_actor[actor] += 1

        created_at = event.get("created_at")
        if created_at:
            ts = _iso_to_dt(created_at)
            if latest_seen is None or ts > latest_seen:
                latest_seen = ts

        if event_type in crypto_types:
            payload = event.get("payload") or {}
            crypto_events.append(
                {
                    "type": event_type,
                    "actor": actor,
                    "repo": (event.get("repo") or {}).get("name", "unknown"),
                    "created_at": created_at,
                    "details": {
                        k: payload.get(k)
                        for k in ("ref", "ref_type", "action", "number", "pull_request", "release", "issue")
                        if payload.get(k) is not None
                    },
                }
            )

    return {
        "total_events": sum(event_counts.values()),
        "unique_actors": len(usage_by_actor),
        "top_actors": usage_by_actor.most_common(5),
        "event_counts": event_counts.most_common(),
        "crypto_events": crypto_events,
        "latest_seen": latest_seen.isoformat() if latest_seen else None,
    }


def summarize_key_usage(owner: str, repo: str) -> Dict[str, Any]:
    events = _fetch_repo_events(owner, repo)
    return _summarize_events(events)


def main() -> None:
    owner = os.getenv("GITHUB_OWNER")
    repo = os.getenv("GITHUB_REPO")
    if not owner or not repo:
        raise SystemExit("Set GITHUB_OWNER and GITHUB_REPO")

    summary = summarize_key_usage(owner, repo)
    print(summary)


if __name__ == "__main__":
    main()
