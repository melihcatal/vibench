import argparse
import os
from collections import Counter
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Iterable, List, Optional

import requests


SENTRY_BASE_URL = os.getenv("SENTRY_BASE_URL", "https://sentry.io/api/0")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--org", default=os.getenv("SENTRY_ORG"))
    parser.add_argument("--project", default=os.getenv("SENTRY_PROJECT"))
    parser.add_argument("--auth-token", default=os.getenv("SENTRY_AUTH_TOKEN"))
    parser.add_argument("--hours", type=int, default=24)
    parser.add_argument("--limit", type=int, default=100)
    return parser.parse_args()


def _headers(auth_token: str) -> Dict[str, str]:
    return {"Authorization": f"Bearer {auth_token}", "Accept": "application/json"}


def _get_json(url: str, auth_token: str, params: Optional[Dict[str, Any]] = None) -> Any:
    response = requests.get(url, headers=_headers(auth_token), params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def _normalize_events(payload: Any) -> List[Dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        for key in ("data", "events", "results"):
            value = payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
    return []


def fetch_error_events(org: str, project: str, auth_token: str, hours: int, limit: int) -> List[Dict[str, Any]]:
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=hours)
    url = f"{SENTRY_BASE_URL}/projects/{org}/{project}/events/"
    params = {
        "query": "level:error",
        "statsPeriod": f"{hours}h",
        "per_page": limit,
        "sort": "-timestamp",
    }
    payload = _get_json(url, auth_token, params=params)
    events = _normalize_events(payload)
    filtered: List[Dict[str, Any]] = []
    for event in events:
        timestamp = event.get("dateCreated") or event.get("timestamp")
        if isinstance(timestamp, str):
            try:
                parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            except ValueError:
                parsed = None
            if parsed is not None and parsed < start:
                continue
        filtered.append(event)
    return filtered


def _extract_message(event: Dict[str, Any]) -> str:
    message = event.get("message") or event.get("title") or "unknown"
    return str(message)


def _extract_fingerprint(event: Dict[str, Any]) -> str:
    for key in ("culprit", "logger", "transaction"):
        value = event.get(key)
        if value:
            return str(value)
    return _extract_message(event)


def summarize_events(events: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    events_list = list(events)
    by_message = Counter(_extract_message(event) for event in events_list)
    by_fingerprint = Counter(_extract_fingerprint(event) for event in events_list)
    first_seen = None
    last_seen = None
    for event in events_list:
        ts = event.get("dateCreated") or event.get("timestamp")
        if isinstance(ts, str):
            try:
                parsed = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            except ValueError:
                continue
            first_seen = parsed if first_seen is None or parsed < first_seen else first_seen
            last_seen = parsed if last_seen is None or parsed > last_seen else last_seen
    return {
        "total_events": len(events_list),
        "top_messages": by_message.most_common(5),
        "top_fingerprints": by_fingerprint.most_common(5),
        "first_seen": first_seen.isoformat() if first_seen else None,
        "last_seen": last_seen.isoformat() if last_seen else None,
    }


def format_summary(summary: Dict[str, Any]) -> str:
    lines = [f"total_errors: {summary['total_events']}"]
    if summary["first_seen"]:
        lines.append(f"first_seen: {summary['first_seen']}")
    if summary["last_seen"]:
        lines.append(f"last_seen: {summary['last_seen']}")
    lines.append("top_messages:")
    for message, count in summary["top_messages"]:
        lines.append(f"  - {count}x {message}")
    lines.append("top_fingerprints:")
    for fingerprint, count in summary["top_fingerprints"]:
        lines.append(f"  - {count}x {fingerprint}")
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    if not args.org or not args.project or not args.auth_token:
        raise RuntimeError("SENTRY_ORG, SENTRY_PROJECT, and SENTRY_AUTH_TOKEN are required")
    events = fetch_error_events(args.org, args.project, args.auth_token, args.hours, args.limit)
    summary = summarize_events(events)
    print(format_summary(summary))


if __name__ == "__main__":
    main()
