import json
from typing import Dict, Any


def summarize(message_records: list[Dict[str, Any]]) -> Dict[str, Any]:
    """Create a summary report from a collection of processed message records.

    Each record is expected to contain at least:
        - id (unique identifier)
        - status (e.g., 'delivered', 'dead_letter')
        - timestamp (ISO string)
    The summary includes counts per status, total processed, and earliest/latest timestamps.
    """
    if not message_records:
        return {"count": 0, "statuses": {}, "earliest": None, "latest": None}

    status_counts = {}
    timestamps = []
    for rec in message_records:
        status = rec.get("status", "unknown")
        status_counts[status] = status_counts.get(status, 0) + 1
        ts = rec.get("timestamp")
        if ts:
            timestamps.append(ts)

    summary = {
        "count": len(message_records),
        "statuses": status_counts,
    }
    if timestamps:
        summary["earliest"] = min(timestamps)
        summary["latest"] = max(timestamps)
    return summary


if __name__ == "__main__":
    # Example usage: load a JSON file of records and print summary
    import pathlib, datetime

    records_path = pathlib.Path("processed_messages.json")
    if records_path.is_file():
        with records_path.open() as f:
            records = json.load(f)
        summary = summarize(records)
        print("Message processing summary:", json.dumps(summary, indent=2))
    else:
        print("No processed_messages.json file found.")
