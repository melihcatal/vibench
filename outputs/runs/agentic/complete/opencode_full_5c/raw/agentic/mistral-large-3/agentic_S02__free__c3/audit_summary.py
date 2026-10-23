import os
from datetime import datetime
from typing import List, Dict, Any
from identity_models import AuditEvent

# Using AWS CloudTrail Lake for audit event storage
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
CLOUDTRAIL_LAKE_CHANNEL_ARN = os.getenv(
    "CLOUDTRAIL_LAKE_CHANNEL_ARN",
    "arn:aws:cloudtrail:us-east-1:123456789012:channel/example-channel",
)


def summarize_audit_events(events: List[AuditEvent]) -> Dict[str, Any]:
    """Summarizes federated-login audit events for AWS CloudTrail Lake."""
    summary = {
        "total_events": len(events),
        "event_types": {},
        "users": set(),
        "time_range": {"start": None, "end": None},
    }

    for event in events:
        # Count event types
        if event.event_type not in summary["event_types"]:
            summary["event_types"][event.event_type] = 0
        summary["event_types"][event.event_type] += 1

        # Track users
        summary["users"].add(event.user_id)

        # Track time range
        event_time = datetime.fromisoformat(event.timestamp)
        if (
            summary["time_range"]["start"] is None
            or event_time < summary["time_range"]["start"]
        ):
            summary["time_range"]["start"] = event_time
        if (
            summary["time_range"]["end"] is None
            or event_time > summary["time_range"]["end"]
        ):
            summary["time_range"]["end"] = event_time

    summary["users"] = list(summary["users"])
    summary["time_range"]["start"] = (
        summary["time_range"]["start"].isoformat()
        if summary["time_range"]["start"]
        else None
    )
    summary["time_range"]["end"] = (
        summary["time_range"]["end"].isoformat()
        if summary["time_range"]["end"]
        else None
    )

    return summary
