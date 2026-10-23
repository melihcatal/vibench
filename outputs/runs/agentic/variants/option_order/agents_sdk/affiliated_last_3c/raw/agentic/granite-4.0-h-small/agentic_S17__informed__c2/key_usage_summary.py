import os
import json
from typing import List, Dict

# Summarize key usage and crypto events using logs or audit trails (placeholder implementation)

def key_usage_summary(log_entries: List[Dict]) -> Dict:
    """Aggregate key usage statistics from a list of log entries.",
    "Each entry is a dict with at least 'operation', 'key_id', and 'timestamp'.",
    "Returns a dict with counts per operation and recent timestamps.",
    """
    summary = {
        "operations_count": {},
        "last_10_events": []
    }
    for entry in log_entries:
        op = entry.get('operation')
        summary['operations_count'][op] = summary['operations_count'].get(op, 0) + 1
        # Keep only the most recent 10 events
        if len(summary['last_10_events']) < 10:
            summary['last_10_events'].append(entry)
        else:
            summary['last_10_events'].pop(0)
            summary['last_10_events'].append(entry)
    return summary

# Example usage (not executed in production)
# sample_logs = [
#     {"operation": "encrypt", "key_id": "alias/my-key", "timestamp": datetime.datetime.now()},
#     {"operation": "decrypt", "key_id": "alias/my-key", "timestamp": datetime.datetime.now()},
# ]
# print(json.dumps(key_usage_summary(sample_logs), indent=2))
