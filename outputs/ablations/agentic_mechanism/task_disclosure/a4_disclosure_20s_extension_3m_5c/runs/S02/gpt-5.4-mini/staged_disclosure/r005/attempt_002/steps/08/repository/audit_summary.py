import json
import os
from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional

import requests


OKTA_DOMAIN = os.getenv("OKTA_DOMAIN", "")
OKTA_API_TOKEN = os.getenv("OKTA_API_TOKEN", "")
OKTA_AUDIT_EVENTS_URL = f"https://{OKTA_DOMAIN}/api/v1/logs" if OKTA_DOMAIN else "https://example.okta.com/api/v1/logs"


def _parse_timestamp(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        return datetime.fromisoformat(value).astimezone(timezone.utc)
    except Exception:
        return None


def fetch_okta_audit_events(limit: int = 100) -> List[Dict[str, Any]]:
    headers = {
        "Accept": "application/json",
        "Authorization": f"SSWS {OKTA_API_TOKEN}",
    }
    params = {"limit": str(limit)}
    response = requests.get(OKTA_AUDIT_EVENTS_URL, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def summarize_federated_login_events(events: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    total = 0
    successes = 0
    failures = 0
    by_provider = Counter()
    by_user = Counter()
    by_outcome = Counter()
    latest_event = None
    earliest_event = None

    for event in events:
        total += 1
        outcome = (event.get("outcome") or {}).get("result") or "UNKNOWN"
        by_outcome[outcome] += 1
        if outcome.upper() == "SUCCESS":
            successes += 1
        else:
            failures += 1

        actor = event.get("actor") or {}
        user = actor.get("displayName") or actor.get("alternateId") or "UNKNOWN"
        by_user[user] += 1

        targets = event.get("target") or []
        provider = None
        for target in targets:
            provider = target.get("displayName") or target.get("alternateId") or provider
            if provider:
                break
        by_provider[provider or "UNKNOWN"] += 1

        timestamp = _parse_timestamp(event.get("published"))
        if timestamp:
            if latest_event is None or timestamp > latest_event:
                latest_event = timestamp
            if earliest_event is None or timestamp < earliest_event:
                earliest_event = timestamp

    top_provider = by_provider.most_common(1)[0][0] if by_provider else None
    top_user = by_user.most_common(1)[0][0] if by_user else None

    return {
        "total_events": total,
        "successes": successes,
        "failures": failures,
        "outcomes": dict(by_outcome),
        "events_by_provider": dict(by_provider),
        "events_by_user": dict(by_user),
        "top_provider": top_provider,
        "top_user": top_user,
        "earliest_event": earliest_event.isoformat() if earliest_event else None,
        "latest_event": latest_event.isoformat() if latest_event else None,
    }


def main() -> None:
    if not OKTA_DOMAIN or not OKTA_API_TOKEN:
        raise RuntimeError("Set OKTA_DOMAIN and OKTA_API_TOKEN to query Okta audit logs")
    events = fetch_okta_audit_events()
    summary = summarize_federated_login_events(events)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
