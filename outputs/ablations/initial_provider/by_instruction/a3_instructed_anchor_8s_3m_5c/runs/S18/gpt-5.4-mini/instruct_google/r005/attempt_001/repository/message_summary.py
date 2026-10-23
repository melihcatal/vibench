from collections import Counter
from typing import Iterable, Mapping

from messaging_models import normalize_payload


def summarize_messages(messages: Iterable[Mapping[str, object]]) -> dict:
    items = [normalize_payload(message) for message in messages]
    return {
        "count": len(items),
        "keys": sorted({key for item in items for key in item.keys()}),
        "types": Counter(type(value).__name__ for item in items for value in item.values()),
    }
