import json
from observability_client import get_log_client
from datetime import datetime
from observability_models import LogEvent

def incident_summary(start_time: datetime | None = None, end_time: datetime | None = None, log_service: str = "datadog") -> str:
    """Summarize error‑log findings for incident review.

    Collects recent errors, groups by error message, and returns a concise markdown report.
    """
    client = get_log_client(log_service)
    # Pull all ERROR logs in the requested window
    raw_logs = client.search_logs({
        "filter": {"level": "ERROR"},
        "time_range": {
            "start": start_time.isoformat() if start_time else "-1h",
            "end": end_time.isoformat() if end_time else "now"
        }
    })["logs"]

    # Group by message text (normalize whitespace)
    groups = {}
    for entry in raw_logs:
        msg = entry["message"].strip()
        groups.setdefault(msg, []).append(entry)

    # Build markdown summary
    lines = ["# Incident Log Summary", ""]
    for msg, entries in groups.items():
        count = len(entries)
        lines.append(f"**{count} occurrences** of:\n")
        lines.append(f"```
{msg}
```")
        lines.append(f"Timestamps: {', '.join(e['timestamp'] for e in entries[:3])} ...")
        lines.append("---")
    return "\n".join(lines)
