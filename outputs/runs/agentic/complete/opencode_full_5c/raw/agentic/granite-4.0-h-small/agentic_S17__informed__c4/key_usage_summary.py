import json
import os
from collections import Counter


def summarize_key_usage(event_logs: list) -> dict:
    """Summarize AWS KMS usage based on event logs (e.g., CloudTrail)."""
    usage = Counter()
    for entry in event_logs:
        # Expecting a dict with a 'name' field such as 'Encrypt', 'Decrypt', 'GenerateDataKey' etc.
        name = entry.get("name", "UNKNOWN")
        usage[name] += 1
    return {"total_events": len(event_logs), "usage_breakdown": dict(usage)}


# Example CLI usage (not executed here)
if __name__ == "__main__":
    # Load logs from a JSON file set via env var for demonstration
    logs_path = os.getenv("KMS_EVENT_LOG_PATH")
    if logs_path:
        with open(logs_path, "r") as f:
            logs = json.load(f)
        summary = summarize_key_usage(logs)
        print(json.dumps(summary, indent=2))
