import os
from typing import List
from observability_models import LogEvent
from observability_client import get_datadog_client

def summarize_error_logs(logs: List[dict]) -> str:
    """Produce a concise incident summary from a list of Datadog log records.

    Focuses on error logs, extracts timestamps, services, and key messages.
    Returns a formatted human‑readable summary string.
    """
    if not logs:
        return 'No error logs found.\n'
    # Assume logs are already filtered for errors (you could add severity filter here)
    timeline = []
    for l in logs:
        ts = l.get('timestamp')
        svc = l.get('service', 'unknown')
        msg = l.get('message', '').strip()[:200]
        timeline.append(f'[{ts}] {svc}: {msg}')
    summary = '=== Error Log Summary ===\n' + '\n'.join(timeline) + '\n=== End ==='
    return summary
