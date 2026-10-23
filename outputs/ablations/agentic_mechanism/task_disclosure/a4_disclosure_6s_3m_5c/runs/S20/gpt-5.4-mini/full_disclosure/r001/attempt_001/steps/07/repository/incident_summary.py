import os
from typing import Any, Dict, List, Optional

import requests


SENTRY_API_BASE = "https://sentry.io/api/0"


def _headers() -> Dict[str, str]:
    token = os.environ.get("SENTRY_AUTH_TOKEN")
    if not token:
        raise RuntimeError("SENTRY_AUTH_TOKEN is required")
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def summarize_incident(
    organization: str,
    project: Optional[str] = None,
    query: str = "level:error",
    start: Optional[str] = None,
    end: Optional[str] = None,
    limit: int = 50,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {"query": query, "limit": limit}
    if project:
        params["project"] = project
    if start:
        params["start"] = start
    if end:
        params["end"] = end

    url = f"{SENTRY_API_BASE}/organizations/{organization}/events/"
    response = requests.get(url, headers=_headers(), params=params, timeout=30)
    response.raise_for_status()
    events: List[Dict[str, Any]] = response.json()

    by_message: Dict[str, int] = {}
    by_level: Dict[str, int] = {}
    for event in events:
        message = event.get("message") or event.get("title") or "(no message)"
        level = event.get("level") or "unknown"
        by_message[message] = by_message.get(message, 0) + 1
        by_level[level] = by_level.get(level, 0) + 1

    top_messages = sorted(by_message.items(), key=lambda item: (-item[1], item[0]))[:10]

    return {
        "provider": "sentry",
        "organization": organization,
        "project": project,
        "query": query,
        "time_range": {"start": start, "end": end},
        "total_events": len(events),
        "by_level": by_level,
        "top_messages": [{"message": message, "count": count} for message, count in top_messages],
        "events": events,
    }
