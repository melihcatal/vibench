import json


def summarize_audit_events(audit_events):
    summary = {}
    for event in audit_events:
        if event["provider_id"] not in summary:
            summary[event["provider_id"]] = {"success": 0, "failure": 0}
        if event["status"] == "success":
            summary[event["provider_id"]]["success"] += 1
        else:
            summary[event["provider_id"]]["failure"] += 1
    return json.dumps(summary, indent=4)