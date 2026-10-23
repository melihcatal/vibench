import os
import json
from pathlib import Path

# Assume provider SDK or REST client is configured elsewhere (e.g., messaging_client.py)
from messaging_client import get_consumer

SUMMARY_FILE = os.getenv("SUMMARY_FILE", "processed_summary.json")

SUMMARY_RECORDS = []


def log_summary(record: dict) -> None:
    """Append a summarized processing record to a JSON line file."""
    with open(SUMMARY_FILE, "a") as f:
        f.write(json.dumps(record) + "\n")
        print(f"Logged summary record: {record}")


def aggregate_summary() -> dict:
    """Read all summary records and aggregate counts.

    Returns:
        dict: Summary with total processed and failure counts.
    """
    if not Path(SUMMARY_FILE).exists():
        return {"processed_total": 0, "failed_total": 0}
    processed = 0
    failed = 0
    with open(SUMMARY_FILE, "r") as f:
        for line in f:
            data = json.loads(line.strip())
            if data.get("status") == "ok":
                processed += 1
            else:
                failed += 1
    return {"processed_total": processed, "failed_total": failed}


if __name__ == "__main__":
    # Example: ingest one message, summarize, and record
    consumer = get_consumer()
    msg = consumer.poll(timeout=1.0)
    if msg and not msg.error():
        payload = json.loads(msg.value())
        # Simulate processing result
        result = True  # or False on failure
        status = "ok" if result else "failed"
        record = {
            "message_id": payload.get("id"),
            "status": status,
            "processed_at": int(1) if result else None,
        }
        log_summary(record)
        # Re-aggregate for demo
        print("Aggregated summary:", aggregate_summary())
