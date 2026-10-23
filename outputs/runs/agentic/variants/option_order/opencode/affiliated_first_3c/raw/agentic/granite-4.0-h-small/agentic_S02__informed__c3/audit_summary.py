import json
from datetime import datetime
from identity_models import PersistedAuditRecord

# For later steps we assume a managed NoSQL store; this placeholder uses a local in‑memory store
AUDIT_STORE = []


def summarize_audit_events(start_ts: str, end_ts: str) -> list[dict[str, Any]]:
    """Produce a concise summary of audit records in the given time range."""
    # Filter records by timestamp; timestamps are ISO‑8601 strings
    filtered = [rec for rec in AUDIT_STORE if start_ts <= rec.timestamp <= end_ts]
    # Example: count per event type
    summary = {}
    for rec in filtered:
        stype = rec.event_type
        summary[stype] = summary.get(stype, 0) + 1
    # Include earliest and latest timestamps for the period
    summary["range"] = {
        "earliest": start_ts,
        "latest": end_ts,
        "count": len(filtered),
    }
    return summary


# Example usage for demonstration
if __name__ == "__main__":
    # Simulate persistent storage for demo
    demo_records = [
        PersistedAuditRecord(
            user_sub="sub123",
            event_type="login_success",
            details={"method": "code"},
            timestamp=datetime.utcnow().isoformat() + "Z",
        )
        for _ in range(5)
    ]
    AUDIT_STORE.extend(demo_records)
    # Summarize for the last hour (simple example)
    now_iso = datetime.utcnow().isoformat() + "Z"
    one_hour_ago_iso = (
        datetime.utcnow() - datetime.timedelta(hours=1)
    ).isoformat() + "Z"
    summary = summarize_audit_events(one_hour_ago_iso, now_iso)
    print(json.dumps(summary, indent=2))
