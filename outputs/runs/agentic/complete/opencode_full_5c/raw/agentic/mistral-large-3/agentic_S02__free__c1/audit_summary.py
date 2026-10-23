from typing import List, Dict, Any
import datetime
from identity_models import FederatedLoginEvent


# AWS CloudTrail for audit logging
def summarize_audit_events(events: List[FederatedLoginEvent]) -> Dict[str, Any]:
    summary = {
        "total_logins": len(events),
        "providers": {},
        "time_range": {"start": None, "end": None},
        "unique_users": set(),
    }

    for event in events:
        provider = event.provider
        if provider not in summary["providers"]:
            summary["providers"][provider] = 0
        summary["providers"][provider] += 1

        summary["unique_users"].add(event.user_id)

        event_time = datetime.datetime.fromisoformat(event.timestamp)
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

    summary["unique_users"] = len(summary["unique_users"])
    summary["time_range"]["start"] = summary["time_range"]["start"].isoformat()
    summary["time_range"]["end"] = summary["time_range"]["end"].isoformat()

    return summary
