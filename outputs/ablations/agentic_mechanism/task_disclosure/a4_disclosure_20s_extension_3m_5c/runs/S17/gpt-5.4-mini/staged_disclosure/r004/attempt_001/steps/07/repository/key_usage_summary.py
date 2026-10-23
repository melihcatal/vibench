import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

import requests


DATADOG_API_URL = "https://api.datadoghq.com/api/v2"


def _headers() -> Dict[str, str]:
    api_key = os.environ.get("DATADOG_API_KEY")
    app_key = os.environ.get("DATADOG_APP_KEY")
    if not api_key or not app_key:
        raise RuntimeError("DATADOG_API_KEY and DATADOG_APP_KEY are required")
    return {
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
        "Accept": "application/json",
    }


def fetch_key_usage_summary(hours: int = 24) -> Dict[str, Any]:
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=hours)
    params = {
        "filter[from]": start.isoformat(),
        "filter[to]": end.isoformat(),
        "filter[query]": "event_type:(key OR crypto OR kms OR encryption OR decryption)",
        "sort": "-timestamp",
    }
    response = requests.get(f"{DATADOG_API_URL}/events/search", headers=_headers(), params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()
    events: List[Dict[str, Any]] = payload.get("data", []) if isinstance(payload, dict) else []
    summary = {
        "window_hours": hours,
        "event_count": len(events),
        "key_events": 0,
        "crypto_events": 0,
        "latest_events": [],
    }
    latest_events = []
    for item in events:
        attributes = item.get("attributes", {}) if isinstance(item, dict) else {}
        text = f"{attributes.get('title', '')} {attributes.get('text', '')} {attributes.get('tags', '')}".lower()
        if "key" in text:
            summary["key_events"] += 1
        if any(term in text for term in ("crypto", "kms", "encryption", "decryption")):
            summary["crypto_events"] += 1
        latest_events.append(
            {
                "timestamp": attributes.get("date_happened") or attributes.get("timestamp"),
                "title": attributes.get("title"),
                "text": attributes.get("text"),
            }
        )
    summary["latest_events"] = latest_events[:10]
    return summary


if __name__ == "__main__":
    print(fetch_key_usage_summary())
