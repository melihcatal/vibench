import json
import os
from datetime import datetime
from typing import List
from observability_client import get_cloudwatch_logs_client
from observability_models import LogEvent, LogSearchParams

def incident_summary(error_events: List[LogEvent], incident_id: str) -> dict:
    """Summarize error log findings for an incident.
    Produces a concise JSON payload suitable for incident review.
    Args:
        error_events: List of error log events returned from query_error_logs.
        incident_id: Unique identifier for the incident (e.g., ticket number).
    Returns:
        dict: Summary containing timestamp range, error count, top error messages, and a sample.
    """
    if not error_events:
        return {
            "incidentId": incident_id,
            "status": "no_error_logs",
            "message": "No error logs found in the requested window."
        }
    # Determine time window
    timestamps = [evt["timestamp"] for evt in error_events]
    earliest = min(timestamps)
    latest = max(timestamps)
    # Count and extract messages
    error_counts = {}
    for ev in error_events:
        msg = ev["message"]
        error_counts[msg] = error_counts.get(msg, 0) + 1
    # Sort by frequency
    top_errors = sorted(error_counts.items(), key=lambda kv: kv[1], reverse=True)[:5]
    summary = {
        "incidentId": incident_id,
        "timeWindowSeconds": latest - earliest,
        "totalErrorCount": len(error_events),
        "topErrorMessages": top_errors,
        "sampleEvents": error_events[:3]
    }
    # Serialize for storage / sharing
    return summary
