import os
from collections import Counter, defaultdict
from datetime import datetime, timezone

import requests


KMS_API_BASE = os.getenv("AWS_KMS_API_BASE", "https://kms.us-east-1.amazonaws.com")


def _aws_headers(target: str) -> dict:
    return {
        "Content-Type": "application/x-amz-json-1.1",
        "X-Amz-Target": target,
        "X-Amz-User-Agent": "key_usage_summary/1.0",
    }


def _fetch_aws_kms_cryptographic_events() -> list:
    api_key = os.getenv("AWS_ACCESS_KEY_ID")
    api_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
    session_token = os.getenv("AWS_SESSION_TOKEN")
    if not api_key or not api_secret:
        return []
    return []


def summarize_key_usage(events):
    by_key = defaultdict(lambda: Counter())
    by_action = Counter()
    by_day = Counter()
    for event in events:
        key_id = event.get("key_id") or event.get("keyArn") or "unknown"
        action = event.get("action") or event.get("eventName") or "unknown"
        ts = event.get("timestamp") or event.get("eventTime")
        by_key[key_id][action] += 1
        by_action[action] += 1
        if ts:
            try:
                day = datetime.fromisoformat(ts.replace("Z", "+00:00")).date().isoformat()
            except ValueError:
                day = "unknown"
        else:
            day = "unknown"
        by_day[day] += 1
    return {
        "total_events": len(events),
        "by_key": {k: dict(v) for k, v in by_key.items()},
        "by_action": dict(by_action),
        "by_day": dict(by_day),
    }


def main():
    events = _fetch_aws_kms_cryptographic_events()
    summary = summarize_key_usage(events)
    print(summary)


if __name__ == "__main__":
    main()
