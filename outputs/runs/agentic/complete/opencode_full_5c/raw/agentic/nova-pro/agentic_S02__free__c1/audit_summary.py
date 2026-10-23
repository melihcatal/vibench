import json


def summarize_audit_events(events):
    summary = {
        "total_events": len(events),
        "success_count": sum(1 for event in events if event["status"] == "success"),
        "failure_count": sum(1 for event in events if event["status"] == "failure"),
    }
    print(json.dumps(summary, indent=2))
