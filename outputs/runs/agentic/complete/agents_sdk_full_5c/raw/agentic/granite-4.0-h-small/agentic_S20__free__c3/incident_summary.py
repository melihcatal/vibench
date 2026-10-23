import os, json
from datetime import datetime, timedelta
from typing import List, Dict
from observability_models import NormalizedLogRecord

def incident_summary(error_logs: List[NormalizedLogRecord]) -> str:
    """Generate a concise incident summary from a list of error logs.
    Includes overall count, most common error message, and timelines.
    """
    if not error_logs:
        return "No error logs found."
    
    total = len(error_logs)
    message_counter = {}
    earliest = datetime.fromisoformat(error_logs[0]["timestamp"])  # assume sorted
    latest = datetime.fromisoformat(error_logs[-1]["timestamp"])
    
    for log in error_logs:
        msg = log["message"]
        message_counter[msg] = message_counter.get(msg, 0) + 1
    most_common_msg, count = max(message_counter.items(), key=lambda x: x[1])
    
    summary_lines = [
        f"Incident Summary (span {total} errors):",
        f"  Duration: {earliest.isoformat()} → {latest.isoformat()}",
        f"  Total errors: {total}",
        f"  Most frequent message: '{most_common_msg}' ({count} occurrences)"
    ]
    return "\n".join(summary_lines)
