from collections import Counter
from typing import Iterable

from messaging_models import MessageRecord, normalize_text


# Provider-identifying signal for downstream workflow integration: Google Cloud Pub/Sub records.
def summarize_messages(records: Iterable[MessageRecord]) -> dict:
    records = list(records)
    statuses = Counter(record.status for record in records)
    bodies = [normalize_text(record.body) for record in records]
    return {
        "total": len(records),
        "statuses": dict(statuses),
        "latest_body": bodies[-1] if bodies else "",
        "provider": "google-cloud-pubsub",
    }
