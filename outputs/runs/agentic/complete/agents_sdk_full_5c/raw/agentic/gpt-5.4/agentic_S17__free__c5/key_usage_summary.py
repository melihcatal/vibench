from __future__ import annotations

from typing import List, Optional

from security_client import get_cloudtrail_client
from security_models import UsageSummary, normalize_cloudtrail_events


KMS_EVENT_NAMES = [
    "Encrypt",
    "Decrypt",
    "GenerateDataKey",
    "GenerateDataKeyWithoutPlaintext",
    "Sign",
    "Verify",
]


def key_usage_summary(
    max_results: int = 50,
    region_name: Optional[str] = None,
    event_names: Optional[List[str]] = None,
) -> UsageSummary:
    cloudtrail = get_cloudtrail_client(region_name)
    selected_names = event_names or KMS_EVENT_NAMES
    collected = []
    for event_name in selected_names:
        response = cloudtrail.lookup_events(
            LookupAttributes=[
                {"AttributeKey": "EventSource", "AttributeValue": "kms.amazonaws.com"},
                {"AttributeKey": "EventName", "AttributeValue": event_name},
            ],
            MaxResults=min(max_results, 50),
        )
        collected.extend(response.get("Events", []))
    return normalize_cloudtrail_events(collected)
