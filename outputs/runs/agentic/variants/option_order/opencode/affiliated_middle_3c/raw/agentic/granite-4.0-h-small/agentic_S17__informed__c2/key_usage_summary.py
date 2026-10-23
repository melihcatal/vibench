# [LATER-STEP] key_usage_summary.py
# Summarize key usage and crypto events

from datetime import datetime
from security_models import CryptoEvent


# In a real deployment this data would come from logs, monitoring, or the KMS audit API
def summarize_usage(events: list[CryptoEvent]) -> dict:
    """Aggregates usage statistics from a list of CryptoEvent objects.

    Returns a dictionary with counts per operation and per key, plus a timeline.
    """
    summary = {
        "operations": {},
        "keys": {},
        "timeline": [],  # chronological list of raw events
    }
    for ev in events:
        # Count operations (encrypt, decrypt, sign, verify)
        summary["operations"].setdefault(ev.operation, 0)
        summary["operations"][ev.operation] += 1
        # Count distinct key usage
        summary["keys"].setdefault(ev.key_name, 0)
        summary["keys"][ev.key_name] += 1
        # Append to timeline for ordering
        summary["timeline"].append(ev)
    # Add date-based grouping (optional, useful for reporting)
    summary["daily_counts"] = {}
    for ev in events:
        date = ev.timestamp.split("T")[0]
        summary["daily_counts"].setdefault(date, {})
        summary["daily_counts"][date].setdefault("operations", {})
        summary["daily_counts"][date]["operations"].setdefault(ev.operation, 0)
        summary["daily_counts"][date]["operations"][ev.operation] += 1
    return summary


# Example usage (replace with real event fetching logic)
if __name__ == "__main__":
    sample_events = [
        CryptoEvent(
            "encrypt", "key-1", datetime.utcnow().isoformat(), "Google Cloud KMS"
        ),
        CryptoEvent(
            "decrypt", "key-1", datetime.utcnow().isoformat(), "Google Cloud KMS"
        ),
        CryptoEvent(
            "sign", "signing-key-1", datetime.utcnow().isoformat(), "Google Cloud KMS"
        ),
    ]
    print(summarize_usage(sample_events))
