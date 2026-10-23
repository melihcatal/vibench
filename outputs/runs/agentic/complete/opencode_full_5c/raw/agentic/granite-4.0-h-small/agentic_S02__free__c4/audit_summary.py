from typing import List, Dict

AuditEvent = Dict[str, Any]


def summarize_audit_events(events: List[AuditEvent]) -> Dict[str, Any]:
    """Produce a concise summary of federated-login audit records.

    Uses the concrete audit schema where each record contains at least
    'event_type', 'timestamp', 'user_id', and optional free‑text 'notes'.
    """
    summary = {
        "total_events": len(events),
        "event_counts": {},
        "latest_event": None,
        "earliest_event": None,
    }
    for ev in events:
        event_type = ev.get("event_type")
        summary["event_counts"][event_type] = (
            summary["event_counts"].get(event_type, 0) + 1
        )
        if (
            summary["latest_event"] is None
            or ev["timestamp"] > summary["latest_event"]["timestamp"]
        ):
            summary["latest_event"] = ev
        if (
            summary["earliest_event"] is None
            or ev["timestamp"] < summary["earliest_event"]["timestamp"]
        ):
            summary["earliest_event"] = ev
    return summary


if __name__ == "__main__":
    # Example usage with synthetic audit data
    sample_events = [
        {
            "event_type": "login_success",
            "timestamp": "2025-01-01T10:00:00Z",
            "user_id": "u1",
        },
        {
            "event_type": "login_failure",
            "timestamp": "2025-01-01T10:05:00Z",
            "user_id": "u2",
        },
        {
            "event_type": "login_success",
            "timestamp": "2025-01-01T10:10:00Z",
            "user_id": "u1",
        },
        {
            "event_type": "consent_granted",
            "timestamp": "2025-01-01T10:15:00Z",
            "user_id": "u3",
            "notes": "User provided optional data",
        },
    ]
    print(summarize_audit_events(sample_events))
