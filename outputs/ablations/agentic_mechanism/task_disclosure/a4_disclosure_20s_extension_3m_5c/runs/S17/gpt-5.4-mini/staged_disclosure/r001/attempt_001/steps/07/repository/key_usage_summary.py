import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import requests


SPLUNK_BASE_URL = os.getenv("SPLUNK_BASE_URL", "https://api.splunk.com")
SPLUNK_ACCESS_TOKEN = os.getenv("SPLUNK_ACCESS_TOKEN")


def _headers() -> Dict[str, str]:
    headers = {"Accept": "application/json"}
    if SPLUNK_ACCESS_TOKEN:
        headers["Authorization"] = f"Bearer {SPLUNK_ACCESS_TOKEN}"
    return headers


def fetch_crypto_events(query: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
    params = {"limit": str(limit)}
    if query:
        params["query"] = query
    response = requests.get(f"{SPLUNK_BASE_URL.rstrip('/')}/v1/security/crypto/events", headers=_headers(), params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()
    if isinstance(payload, dict):
        if "events" in payload and isinstance(payload["events"], list):
            return payload["events"]
        if "data" in payload and isinstance(payload["data"], list):
            return payload["data"]
    if isinstance(payload, list):
        return payload
    return []


def summarize_key_usage(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    summary = {
        "provider": "Splunk",
        "event_count": len(events),
        "actions": {},
        "keys": {},
        "failures": 0,
        "first_seen": None,
        "last_seen": None,
    }
    for event in events:
        action = str(event.get("action") or event.get("event_type") or event.get("operation") or "unknown")
        key_id = str(event.get("key_id") or event.get("keyId") or event.get("key") or "unknown")
        summary["actions"][action] = summary["actions"].get(action, 0) + 1
        summary["keys"][key_id] = summary["keys"].get(key_id, 0) + 1
        outcome = str(event.get("outcome") or event.get("status") or "").lower()
        if outcome in {"failed", "error", "denied", "blocked"} or event.get("error"):
            summary["failures"] += 1
        ts = event.get("timestamp") or event.get("time") or event.get("created_at")
        if ts:
            parsed = _parse_timestamp(ts)
            if parsed:
                if summary["first_seen"] is None or parsed < summary["first_seen"]:
                    summary["first_seen"] = parsed
                if summary["last_seen"] is None or parsed > summary["last_seen"]:
                    summary["last_seen"] = parsed
    if summary["first_seen"] is not None:
        summary["first_seen"] = summary["first_seen"].isoformat()
    if summary["last_seen"] is not None:
        summary["last_seen"] = summary["last_seen"].isoformat()
    return summary


def _parse_timestamp(value: Any) -> Optional[datetime]:
    if isinstance(value, (int, float)):
        try:
            return datetime.fromtimestamp(float(value), tz=timezone.utc)
        except (OverflowError, OSError, ValueError):
            return None
    if isinstance(value, str):
        text = value.strip()
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        try:
            dt = datetime.fromisoformat(text)
            return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
        except ValueError:
            return None
    return None


def main() -> None:
    events = fetch_crypto_events()
    print(json.dumps(summarize_key_usage(events), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
