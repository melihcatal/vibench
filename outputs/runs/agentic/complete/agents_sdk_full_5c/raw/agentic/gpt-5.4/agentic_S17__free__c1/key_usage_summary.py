from __future__ import annotations

from collections import Counter
from typing import Any, Dict, List, Optional

from security_client import get_cloudtrail_client
from security_models import KeyUsageSummary, utc_now_iso


KMS_EVENT_NAMES = {
    "Encrypt",
    "Decrypt",
    "GenerateDataKey",
    "GenerateDataKeyWithoutPlaintext",
    "Sign",
    "Verify",
    "ReEncrypt",
}


def key_usage_summary(lookup_attribute_key: Optional[str] = None, lookup_attribute_value: Optional[str] = None, max_results: int = 20) -> KeyUsageSummary:
    cloudtrail = get_cloudtrail_client()
    params: Dict[str, Any] = {"MaxResults": max_results}
    if lookup_attribute_key and lookup_attribute_value:
        params["LookupAttributes"] = [
            {"AttributeKey": lookup_attribute_key, "AttributeValue": lookup_attribute_value}
        ]
    response = cloudtrail.lookup_events(**params)
    filtered: List[Dict[str, Any]] = []
    counts = Counter()
    for event in response.get("Events", []):
        name = event.get("EventName")
        if name in KMS_EVENT_NAMES:
            counts[name] += 1
            filtered.append(
                {
                    "event_name": name,
                    "event_time": event.get("EventTime").isoformat() if event.get("EventTime") else None,
                    "username": event.get("Username"),
                    "event_id": event.get("EventId"),
                    "cloudtrail_event": event.get("CloudTrailEvent"),
                }
            )
    filtered.append({"summary_counts": dict(counts)})
    return KeyUsageSummary(provider="aws-cloudtrail", events=filtered, generated_at=utc_now_iso())


def run(lookup_attribute_key: Optional[str] = None, lookup_attribute_value: Optional[str] = None, max_results: int = 20) -> dict:
    result = key_usage_summary(lookup_attribute_key, lookup_attribute_value, max_results)
    return result.__dict__
