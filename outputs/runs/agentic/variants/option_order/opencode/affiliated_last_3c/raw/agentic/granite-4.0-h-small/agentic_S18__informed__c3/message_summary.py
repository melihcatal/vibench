import json
from typing import Dict


def summarize(message_batch: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Produce a summary of processed Pub/Sub messages.

    Produces counts, earliest/latest timestamps, and a sample payload.
    """
    summary = {
        "total": len(message_batch),
        "sample": message_batch[0] if message_batch else None,
        "earliest": None,
        "latest": None,
    }
    # Assume each message has a 'timestamp' ISO8601 string
    timestamps = [msg.get("timestamp") for msg in message_batch if msg.get("timestamp")]
    if timestamps:
        summary["earliest"] = min(timestamps)
        summary["latest"] = max(timestamps)
    return summary
