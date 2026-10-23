from collections import Counter
from typing import Any, Dict, Iterable

from google.cloud import pubsub_v1


def summarize_message_processing(records: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    records = list(records)
    statuses = Counter(record.get("status", "unknown") for record in records)
    provider = "google-cloud-pubsub"
    return {"provider": provider, "total": len(records), "status_counts": dict(statuses), "successful": statuses.get("success", 0)}
