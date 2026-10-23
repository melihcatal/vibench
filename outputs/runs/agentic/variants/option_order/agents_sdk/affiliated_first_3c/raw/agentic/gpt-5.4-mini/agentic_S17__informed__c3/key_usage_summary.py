from __future__ import annotations

import os
from collections import Counter
from typing import Any, Dict, List

from security_client import list_crypto_events

AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")


def key_usage_summary() -> Dict[str, Any]:
    events = list_crypto_events(region_name=AWS_REGION)
    by_operation = Counter(event.operation for event in events)
    by_status = Counter(event.status for event in events)
    return {
        "region": AWS_REGION,
        "total_events": len(events),
        "operations": dict(by_operation),
        "statuses": dict(by_status),
        "key_ids": sorted({event.key_id for event in events if event.key_id}),
    }
