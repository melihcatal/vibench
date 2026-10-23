from typing import List, Dict


def summarize_audit_events(events: List[Dict]) -> Dict:
    """
    Summarize federated-login audit events from a managed doc store.
    Returns a dict with counts by event type and a timestamp range.
    """
    summary = {
        "total_events": len(events),
        "unique_event_types": len(set(e["type"] for e in events)),
        "event_types_count": {},
        "time_range": {"earliest": None, "latest": None},
    }
    for ev in events:
        t = ev.get("type")
        summary["event_types_count"][t] = summary["event_types_count"].get(t, 0) + 1
        ts = ev.get("timestamp")
        if ts:
            if (
                summary["time_range"]["earliest"] is None
                or ts < summary["time_range"]["earliest"]
            ):
                summary["time_range"]["earliest"] = ts
            if (
                summary["time_range"]["latest"] is None
                or ts > summary["time_range"]["latest"]
            ):
                summary["time_range"]["latest"] = ts
    return summary


# Example usage (for local testing)
if __name__ == "__main__":
    sample_events = [
        {"type": "login_success", "timestamp": "2024-01-15T12:00:00Z"},
        {"type": "login_failure", "timestamp": "2024-01-15T12:05:00Z"},
        {"type": "login_success", "timestamp": "2024-01-16T09:30:00Z"},
    ]
    print(summarize_audit_events(sample_events))
