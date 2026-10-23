from collections import Counter

from google.cloud import logging_v2

from observability_client import build_client


def incident_summary(payload, config=None):
    client, config = build_client(config)
    entries = list(client.list_entries(filter_=payload["query"], page_size=payload.get("limit", 50)))
    severities = Counter(entry.severity for entry in entries if getattr(entry, "severity", None))
    messages = [entry.payload.get("message") if hasattr(entry, "payload") else None for entry in entries]
    messages = [message for message in messages if message]
    return {"total": len(entries), "severities": dict(severities), "top_messages": messages[:5]}
