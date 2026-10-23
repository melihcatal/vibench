from collections import Counter


def message_summary(payload):
    records = payload.get("records", [])
    statuses = Counter(record.get("status", "unknown") for record in records)
    return {"total": len(records), "statuses": dict(statuses)}
