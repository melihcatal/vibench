import os
from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional

import requests


AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE", "https://api.auth0.com/")
AUTH0_TOKEN = os.getenv("AUTH0_TOKEN", "")


def _auth0_headers() -> Dict[str, str]:
    headers = {"Accept": "application/json"}
    if AUTH0_TOKEN:
        headers["Authorization"] = f"Bearer {AUTH0_TOKEN}"
    return headers


def _auth0_base_url() -> str:
    if not AUTH0_DOMAIN:
        raise ValueError("AUTH0_DOMAIN is required")
    return f"https://{AUTH0_DOMAIN.rstrip('/')}
"


def fetch_auth0_audit_events(limit: int = 100) -> List[Dict[str, Any]]:
    url = f"{_auth0_base_url().strip()}/api/v2/logs"
    params = {"per_page": limit, "sort": "date:-1"}
    response = requests.get(url, headers=_auth0_headers(), params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()
    return payload if isinstance(payload, list) else payload.get("logs", [])


def summarize_federated_login_events(events: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    total = 0
    successful = 0
    failed = 0
    by_connection = Counter()
    by_strategy = Counter()
    by_day = Counter()
    recent_users = []

    for event in events:
        if event.get("type") != "s":
            continue
        description = str(event.get("description", "")).lower()
        strategy = str(event.get("connection", "") or event.get("strategy", "") or "unknown")
        if "federated" not in description and strategy not in {"waad", "samlp", "oidc", "google-oauth2", "github"}:
            continue
        total += 1
        by_connection[event.get("connection", "unknown")] += 1
        by_strategy[event.get("strategy", "unknown")] += 1
        ts = event.get("date")
        if ts:
            try:
                day = datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(timezone.utc).date().isoformat()
                by_day[day] += 1
            except Exception:
                pass
        if event.get("user_id"):
            recent_users.append(event.get("user_id"))
        if event.get("type") == "s":
            successful += 1
        else:
            failed += 1

    return {
        "total_federated_logins": total,
        "successful": successful,
        "failed": failed,
        "top_connections": by_connection.most_common(5),
        "top_strategies": by_strategy.most_common(5),
        "by_day": dict(sorted(by_day.items())),
        "sample_users": recent_users[:10],
    }


def format_summary(summary: Dict[str, Any]) -> str:
    lines = ["Federated login audit summary (Auth0)"]
    lines.append(f"Total federated logins: {summary['total_federated_logins']}")
    lines.append(f"Successful: {summary['successful']}")
    lines.append(f"Failed: {summary['failed']}")
    lines.append("Top connections:")
    for name, count in summary["top_connections"]:
        lines.append(f"- {name}: {count}")
    lines.append("Top strategies:")
    for name, count in summary["top_strategies"]:
        lines.append(f"- {name}: {count}")
    lines.append("By day:")
    for day, count in summary["by_day"].items():
        lines.append(f"- {day}: {count}")
    if summary["sample_users"]:
        lines.append("Sample users:")
        for user in summary["sample_users"]:
            lines.append(f"- {user}")
    return "\n".join(lines)


def main() -> None:
    events = fetch_auth0_audit_events()
    summary = summarize_federated_login_events(events)
    print(format_summary(summary))


if __name__ == "__main__":
    main()
