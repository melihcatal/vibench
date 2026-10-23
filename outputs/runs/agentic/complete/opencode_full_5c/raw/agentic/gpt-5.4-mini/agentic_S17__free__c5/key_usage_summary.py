from collections import Counter
from typing import Iterable, Mapping

from security_client import SecurityClient


def key_usage_summary(events: Iterable[Mapping[str, str]]) -> dict:
    client = SecurityClient()
    counts = Counter()
    for event in events:
        counts[event.get("action", "unknown")] += 1
    return {
        "region": client.region_name,
        "usage": dict(counts),
        "source": "aws-cloudtrail-kms",
    }
