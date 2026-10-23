import datetime
from typing import List, Dict, Any
from .observability_models import LogEvent, ErrorEvent

def incident_summary(error_events: List[ErrorEvent], window_hours: int = 1) -> Dict[str, Any]:
    """Produce a concise markdown summary of recent error logs for incident review.",
    now = datetime.datetime.utcnow()
    cutoff = (now - datetime.timedelta(hours=window_hours)).timestamp()
    # Filter only events within the window (just in case)
    recent = [e for e in error_events if e["timestamp"] >= cutoff]
    summary = {
        "title": "Recent Error Log Summary",
        "time_window_hours": window_hours,
        "count": len(recent),
        "samples": []
    }
    # Grab a few representative examples (max 10)
    for ev in recent[:10]:
        summary["samples"].append({
            "timestamp": datetime.datetime.fromtimestamp(ev["timestamp"]).isoformat() + \"Z\",
            "message": ev["message"],
            "exception": ev.get("exception", ""),
            "stack_trace": ev.get("stack_trace", "")
        })
    return summary