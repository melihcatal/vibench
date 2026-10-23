from collections import Counter


def message_summary(records):
    statuses = Counter(record.get("status", "unknown") for record in records)
    return {"provider": "google.pubsub_v1", "total": len(records), "statuses": dict(statuses)}
