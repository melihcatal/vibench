import os
import json
from typing import List, Dict
from identity_models import AuditEvent

# Constants for the audit log path (in later steps this would be a managed NoSQL store)
AUDIT_LOG_PATH = os.getenv("FEDERATED_LOGIN_AUDIT_FILE", "/tmp/federated_audit.log")


def summarize_audit_events(limit: int = 20) -> List[Dict]:
    """Summarize recent federated‑login audit events into a concise report.
    Reads the audit file line‑by‑line and produces a summary list of the newest events.
    """
    report = []
    try:
        with open(AUDIT_LOG_PATH, "r") as f:
            lines = f.readlines()[-limit:]
    except FileNotFoundError:
        return []  # No audit entries yet

    for raw_line in lines:
        try:
            event: AuditEvent = json.loads(raw_line.strip())
            summary = {
                "event_type": event["event_type"],
                "user_id": event["user_id"],
                "timestamp": event["timestamp"],
                "details": event.get("details", {}),
            }
            report.append(summary)
        except json.JSONDecodeError:
            continue  # malformed line, skip
    return report


if __name__ == "__main__":
    # Example usage – print the last 5 audit summaries
    for entry in summarize_audit_events(5):
        print(entry)
