import os
import json
from datetime import datetime
from typing import List, Dict, Any

from Model.identity_models import LoginAuditEvent

# Provider: Google Identity Platform Audit Log (Cloud Logging)
AUDIT_EXPORT_PATH = os.getenv("GOOGLE_AUDIT_EXPORT_PATH", "audit_logs/google.jsonl")


def summarize_audit_events(events: List[LoginAuditEvent]) -> Dict[str, Any]:
    """Create a high‑level summary of federated‑login audit records.

    Args:
        events: List of raw audit event dicts.

    Returns:
        Dictionary with counts, timestamps, and a few representative details.
    """
    # Provider: Google Identity Platform (structured JSONL)
    total = len(events)
    by_status: Dict[str, int] = {}
    most_recent = None
    for ev in events:
        status = ev.get("status", "unknown")
        by_status[status] = by_status.get(status, 0) + 1
        if most_recent is None or ev["timestamp"] > most_recent["timestamp"]:
            most_recent = ev
    summary = {
        "total_events": total,
        "successful": by_status.get("success", 0),
        "failed": by_status.get("failure", 0),
        "most_recent": most_recent,
    }
    return summary
