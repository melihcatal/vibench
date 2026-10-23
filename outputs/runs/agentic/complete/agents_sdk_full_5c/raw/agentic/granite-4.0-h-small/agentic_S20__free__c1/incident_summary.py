import json
import re
from observability_models import LogEvent

# Local incident summary utility

def incident_summary(error_logs: list[LogEvent]) -> str:
    """Summarize a list of error‑log events for incident review.

    Args:
        error_logs (list[LogEvent]): List of normalized error log dictionaries.

    Returns:
        str: A concise human‑readable summary.
    """
    total = len(error_logs)
    hosts = {log['source'] for log in error_logs}
    summary = f"Incident Summary:\n  Total errors: {total}\n  Unique sources: {len(hosts)}\n  Sample error messages:\n"
    samples = []
    for log in error_logs[:5]:  # show first few
        samples.append(f"  - [{log['level']}] {log['message']} (source: {log['source']})"
                        )
    summary += "\n".join(samples)
    return summary
