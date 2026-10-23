from typing import List, Dict
from datetime import datetime
import uuid
from identity_models import AuditEvent

# AWS CloudTrail for audit logging with concrete model identifier
PROVIDER_NAME = "aws_cloudtrail"
MODEL_ID = "aws-cloudtrail-v1"


def summarize_audit_events(events: List[AuditEvent]) -> Dict:
    """Summarize federated-login audit events for AWS CloudTrail."""
    summary = {
        "total_events": len(events),
        "providers": {},
        "event_types": {},
        "time_range": {"start": None, "end": None},
        "model_id": MODEL_ID,
    }

    for event in events:
        # Update time range
        if (
            summary["time_range"]["start"] is None
            or event.timestamp < summary["time_range"]["start"]
        ):
            summary["time_range"]["start"] = event.timestamp
        if (
            summary["time_range"]["end"] is None
            or event.timestamp > summary["time_range"]["end"]
        ):
            summary["time_range"]["end"] = event.timestamp

        # Count providers
        if event.provider not in summary["providers"]:
            summary["providers"][event.provider] = 0
        summary["providers"][event.provider] += 1

        # Count event types
        if event.event_type not in summary["event_types"]:
            summary["event_types"][event.event_type] = 0
        summary["event_types"][event.event_type] += 1

    return summary
