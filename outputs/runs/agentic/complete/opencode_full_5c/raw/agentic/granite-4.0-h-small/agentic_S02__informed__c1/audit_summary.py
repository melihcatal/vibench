import json
from datetime import datetime
from identity_models import AuditRecord
from managed_store import DocumentStore


def summarize_audit_events(store: DocumentStore, query_filter: dict = None) -> dict:
    """Produce a concise summary of federated login audit events.

    - Counts by event_type (login, token_exchange, callback, etc.)
    - Earliest and latest timestamps
    - Top 5 most active user_ids
    - Overall time range
    Returns a dict with human‑readable summary statistics.
    """
    # Retrieve raw records (most recent first)
    raw_events = store.query(collection="login_audit", filter=query_filter)
    events = [AuditRecord(**item) for item in raw_events]
    if not events:
        return {
            "total_events": 0,
            "event_types": {},
            "time_range": {},
            "top_users": [],
            "summary": "No audit records found.",
        }
    # 1. Event type counts
    type_counts = {}
    for ev in events:
        type_counts[ev.event_type] = type_counts.get(ev.event_type, 0) + 1
    # 2. Timestamp extremes
    timestamps = [ev.timestamp for ev in events]
    earliest = min(timestamps)
    latest = max(timestamps)
    time_range = {
        "earliest": datetime.utcfromtimestamp(earliest / 1000).isoformat() + "Z",
        "latest": datetime.utcfromtimestamp(latest / 1000).isoformat() + "Z",
    }
    # 3. Top 5 users by login count
    user_counts = {}
    for ev in events:
        if ev.event_type == "login":
            user_counts[ev.user_id] = user_counts.get(ev.user_id, 0) + 1
    top_users = sorted(user_counts.items(), key=lambda kv: kv[1], reverse=True)[:5]
    top_users = [{"user_id": uid, "login_count": cnt} for uid, cnt in top_users]
    # 4. Build summary
    summary = {
        "total_events": len(events),
        "event_types": type_counts,
        "time_range": time_range,
        "top_users": top_users,
        "summary": f"Collected {len(events)} login audit events.",
    }
    return summary


# Example usage (would be imported by a scheduled job or API endpoint)
# store = DocumentStore(uri=os.getenv('FIREBASE_FIRESTORE_URI'), collection='login_audit')
# print(json.dumps(summarize_audit_events(store), indent=2))
