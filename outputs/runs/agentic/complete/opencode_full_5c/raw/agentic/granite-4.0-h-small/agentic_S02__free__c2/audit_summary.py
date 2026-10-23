import datetime
import json


def summarize_audit_events(events):
    """
    events: list of dicts with keys: event_type, user_id, timestamp, details (optional)
    Returns a concise summary dict:
        - total_events
        - counts_by_type
        - latest_event (type, user, timestamp)
    """
    total = len(events)
    counts = {}
    latest = None
    for ev in events:
        typ = ev.get("event_type")
        counts[typ] = counts.get(typ, 0) + 1
        if not latest or ev["timestamp"] > latest["timestamp"]:
            latest = ev
    summary = {"total_events": total, "counts_by_type": counts, "latest_event": latest}
    return summary
