from __future__ import annotations

from typing import Any, Dict, List

import boto3

from security_client import load_security_config


def summarize_key_usage(days: int = 7) -> Dict[str, Any]:
    region = load_security_config().region_name
    cloudtrail = boto3.client("cloudtrail", region_name=region)
    kms = boto3.client("kms", region_name=region)

    keys = kms.list_keys().get("Keys", [])
    events: List[Dict[str, Any]] = []
    lookup = cloudtrail.lookup_events(LookupAttributes=[{"AttributeKey": "EventSource", "AttributeValue": "kms.amazonaws.com"}], MaxResults=min(max(days, 1) * 10, 50))
    for event in lookup.get("Events", []):
        events.append({
            "event_name": event.get("EventName"),
            "event_time": event.get("EventTime").isoformat() if event.get("EventTime") else None,
            "username": event.get("Username"),
        })

    return {
        "provider": "AWS KMS",
        "region": region,
        "key_count": len(keys),
        "crypto_events": events,
    }
