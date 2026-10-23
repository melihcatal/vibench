import json


def summarize_audit_events(events):
    summary = {
        "total_events": len(events),
        "success_events": sum(1 for event in events if event["status"] == "success"),
        "failure_events": sum(1 for event in events if event["status"] == "failure")
    }
    return json.dumps(summary, indent=2)
