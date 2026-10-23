import json
from typing import List, Dict
from observability_models import LogEvent
from observability_client import normalize_event


def incident_summary(log_events: List[Dict[str, Any]]) -> str:
    """Summarize error-log findings for incident review.

    Provider: Any managed logging service (example uses the same HEC endpoint).
    """
    error_events = [
        normalize_event(e) for e in log_events if e.get("severity") == "ERROR"
    ]
    summary = [
        f"Incident Summary ({len(error_events)} error(s) detected):",
        "-",
    ]
    for evt in error_events[:10]:  # show first 10 errors
        summary.append(
            f"  * {evt['timestamp']} - {evt['message']} (id={evt['event_id']})"
        )
    if len(error_events) > 10:
        summary.append(f"  ... {len(error_events) - 10} more errors")
    return "\\n".join(summary)
