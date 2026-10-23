from __future__ import annotations

from collections import Counter
from typing import Iterable

from security_models import UsageSummary


def key_usage_summary(events: Iterable[dict], key_id: str) -> dict:
    counts = Counter(event.get("operation") for event in events if event.get("key_id") == key_id)
    summary = UsageSummary(
        key_id=key_id,
        total_operations=sum(counts.values()),
        encryptions=counts.get("encrypt", 0),
        decryptions=counts.get("decrypt", 0),
        signatures=counts.get("sign", 0) + counts.get("verify", 0),
    )
    return summary.__dict__
