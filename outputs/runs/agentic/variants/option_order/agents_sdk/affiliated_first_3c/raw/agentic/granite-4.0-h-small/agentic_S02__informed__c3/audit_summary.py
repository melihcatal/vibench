import os
from typing import List
from identity_models import AuditEvent
from login_audit_store import get_audit_store_client

def summarize_audit_events(event_list: List[AuditEvent]) -> dict:
    """
    Produce a high‑level summary of federated‑login audit events.
    Includes count, latest timestamp, and breakdown by event_type.
    """
    summary = {
        "total_events": len(event_list),
        "latest_timestamp": max(e.timestamp for e in event_list) if event_list else None,
        "by_type": {}
    }
    for ev in event_list:
        summary["by_type"][ev.event_type] = summary["by_type"].get(ev.event_type, 0) + 1
    return summary

if __name__ == "__main__":
    # Example: fetch all audit records and summarize (requires store to be populated)
    client = get_audit_store_client()
    all_events = client.fetch_all()
    result = summarize_audit_events(all_events)
    print("Audit summary:", result)
