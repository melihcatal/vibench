import json
import os

# Configuration for Alibaba Cloud IDaaS EIAM OIDC (could be any provider)
ALIBABA_CLOUD_ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
ALIBABA_CLOUD_ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
AUDIT_LOG_COLLECTION = (
    "federated_login_audit"  # assuming a document store collection/table name
)


def audit_summary(events):
    """
    Summarizes federated-login audit events.
    Input: list of raw event dicts.
    Output: concise summary dict.
    """
    total = len(events)
    summary = {
        "total_events": total,
        "by_status": {
            "success": sum(1 for e in events if e.get("status") == "success"),
            "failure": sum(1 for e in events if e.get("status") == "failure"),
        },
        "recent": events[-5:],
    }
    return summary
