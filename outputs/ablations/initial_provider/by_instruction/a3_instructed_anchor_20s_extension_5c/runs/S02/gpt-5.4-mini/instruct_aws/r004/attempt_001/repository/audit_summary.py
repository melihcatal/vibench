import json
import urllib.request


def summarize_audit_events(events):
    return {
        "event_count": len(events),
        "providers": sorted({event.get("provider", "amazon-cognito") for event in events}),
        "success_count": sum(1 for event in events if event.get("status") == "success"),
        "failure_count": sum(1 for event in events if event.get("status") == "failure"),
    }
