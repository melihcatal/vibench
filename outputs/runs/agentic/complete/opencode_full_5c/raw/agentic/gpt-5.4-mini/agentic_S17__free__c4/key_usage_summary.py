from collections import Counter
from typing import Iterable, Mapping

from security_client import SecurityClient


def key_usage_summary(events: Iterable[Mapping[str, str]]) -> dict:
    client = SecurityClient()
    counts = Counter(event.get("operation", "unknown") for event in events)
    return {
        "provider": client.provider,
        "key_id": client.managed_key_id(),
        "counts": dict(counts),
    }
