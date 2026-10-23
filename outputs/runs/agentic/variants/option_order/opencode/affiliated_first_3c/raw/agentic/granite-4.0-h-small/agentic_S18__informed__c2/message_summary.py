import json
from datetime import datetime
from typing import List, Dict, Any


def summarize_processing(results: List[Dict[str, Any]]) -> str:
    """Create a concise text summary of message processing results.

    Each element in `results` is expected to be a dict produced by the
    `consume_event` helper, with at least a 'status' key ('success' or
    'failure') and optionally a 'timestamp' or 'error' field.

    The summary includes:
      * total number of messages
      * count of successes vs. failures
      * timestamps of first/last processed items
      * a list of error reasons for failures
    """
    total = len(results)
    if total == 0:
        return "No messages processed."
    success_cnt = sum(1 for r in results if r.get("status") == "success")
    failure_cnt = total - success_cnt
    # Find timestamps for earliest/latest processing
    timestamps = [r.get("timestamp", None) for r in results if r.get("timestamp")]
    first = min(timestamps) if timestamps else "<none>"
    last = max(timestamps) if timestamps else "<none>"
    # Gather failure reasons
    failure_reasons = []
    for r in results:
        if r.get("status") != "success":
            reason = r.get("error", "unknown")
            if reason not in failure_reasons:
                failure_reasons.append(reason)
    # Build text summary
    summary_lines = [
        f"Processed {total} message(s) between {first} and {last}.",
        f"Success: {success_cnt}, Failure: {failure_cnt}.",
    ]
    if failure_reasons:
        summary_lines.append(f"Failure reasons: {', '.join(failure_reasons)}.")
    return "\\n".join(summary_lines)


# Example usage (for local testing)
if __name__ == "__main__":
    fake_results = [
        {"status": "success", "timestamp": "2025-08-15T12:00:00Z"},
        {
            "status": "failure",
            "error": "invalid_payload",
            "timestamp": "2025-08-15T12:05:00Z",
        },
        {"status": "success", "timestamp": "2025-08-15T12:10:00Z"},
    ]
    print(summarize_processing(fake_results))
