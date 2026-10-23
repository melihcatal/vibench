from __future__ import annotations

import os
from collections import Counter
from typing import Any, Dict, List

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from security_client import resolve_region


def key_usage_summary(days: int = 7) -> Dict[str, Any]:
    region = resolve_region()
    cloudtrail = boto3.client("cloudtrail", region_name=region)
    try:
        events = cloudtrail.lookup_events(LookupAttributes=[{"AttributeKey": "EventSource", "AttributeValue": "kms.amazonaws.com"}], MaxResults=50).get("Events", [])
        counts = Counter(event.get("EventName", "unknown") for event in events)
        return {"region": region, "days": days, "event_counts": dict(counts), "event_count": len(events)}
    except (ClientError, BotoCoreError) as exc:
        raise RuntimeError(f"AWS CloudTrail lookup failed: {exc}") from exc


def main() -> Dict[str, Any]:
    days = int(os.environ.get("DAYS", "7"))
    return key_usage_summary(days=days)
