# [LATER-STEP] key_usage_summary.py

import json
from collections import Counter

# Example stub: collect usage events from a logging service (e.g., CloudWatch Logs)
# For demo purposes we simulate a list of key IDs used in operations.
USAGE_EVENTS = [
    {
        "operation": "ENCRYPT",
        "key_id": "arn:aws:kms:us-east-1:123456789012:key/abcd1234",
    },
    {
        "operation": "DECRYPT",
        "key_id": "arn:aws:kms:us-east-1:123456789012:key/abcd1234",
    },
    {
        "operation": "ENCRYPT",
        "key_id": "arn:aws:kms:us-east-1:123456789012:key/efgh5678",
    },
    {"operation": "SIGN", "key_id": "arn:aws:kms:us-east-1:123456789012:key/abcd1234"},
]


def summarize_key_usage() -> str:
    """Generate a concise summary of key usage counts."""
    ops = [event["operation"] for event in USAGE_EVENTS]
    counts = Counter(ops)
    lines = [f"Total operations: {len(ops)}"]
    for op, cnt in counts.items():
        lines.append(f"  {op}: {cnt}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(summarize_key_usage())
