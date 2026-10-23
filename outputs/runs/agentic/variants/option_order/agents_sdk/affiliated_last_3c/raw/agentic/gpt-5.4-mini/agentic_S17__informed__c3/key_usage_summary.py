from __future__ import annotations

import os
from collections import Counter
from typing import Iterable

import boto3

from security_models import KeyUsageSummary

PROVIDER = "aws-cloudtrail"


def summarize_key_usage(key_id: str | None = None, event_names: Iterable[str] | None = None) -> KeyUsageSummary:
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    client = boto3.client("cloudtrail", region_name=region)
    lookup = list(event_names or ["Encrypt", "Decrypt", "GenerateDataKey", "Sign", "Verify"])
    counts: Counter[str] = Counter()
    for event_name in lookup:
        response = client.lookup_events(LookupAttributes=[{"AttributeKey": "EventName", "AttributeValue": event_name}], MaxResults=50)
        counts[event_name] = len(response.get("Events", []))
    return KeyUsageSummary(provider=PROVIDER, key_id=key_id or "", operations=dict(counts), metadata={"lookup_events": lookup})
