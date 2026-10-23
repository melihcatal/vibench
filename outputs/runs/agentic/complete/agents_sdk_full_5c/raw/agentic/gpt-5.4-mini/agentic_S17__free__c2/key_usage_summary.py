from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from google.cloud import logging_v2


@dataclass
class UsageSummary:
    counts: Dict[str, int]


def key_usage_summary(resource_name: str) -> UsageSummary:
    client = logging_v2.Client()
    counts = {"encrypt": 0, "decrypt": 0, "sign": 0, "verify": 0}
    for entry in client.list_entries(filter_=f'resource.type="cloud_kms_cryptokey" AND resource.labels.crypto_key_id="{resource_name}"'):
        text = entry.payload if isinstance(entry.payload, str) else str(entry.payload)
        for label in counts:
            if label in text.lower():
                counts[label] += 1
    return UsageSummary(counts=counts)
