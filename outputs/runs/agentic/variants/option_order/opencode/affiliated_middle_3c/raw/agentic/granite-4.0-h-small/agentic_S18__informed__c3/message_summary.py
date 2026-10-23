import json
from datetime import datetime
from typing import Dict, Any

# Azure Service Bus client utilities from helper
from .messaging_client import get_client


def summarize_results(result_records: List[Dict[str, Any]]) -> str:
    """Create a plain‑text summary of Pub/Sub processing results."""
    total = len(result_records)
    successes = sum(1 for r in result_records if r.get("status") == "success")
    failures = total - successes
    summary = (
        f"Pub/Sub processing summary (as of {datetime.utcnow().isoformat()} UTC):\n"
        f"Total messages processed: {total}\n"
        f"Success: {successes}\n"
        f"Failures: {failures}"
    )
    return summary


# Example usage (would be called later in a workflow):
# records = [...]  # list of dicts from consumption / processing
# print(summarize_results(records))
