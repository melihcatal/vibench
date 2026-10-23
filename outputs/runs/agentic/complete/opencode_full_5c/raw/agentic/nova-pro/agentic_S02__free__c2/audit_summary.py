import os
import json


def summarize_audit_events():
    audit_events = [
        {
            "event_id": "1",
            "user_id": "user1",
            "event_type": "login",
            "timestamp": "2023-01-01T12:00:00Z",
        },
        {
            "event_id": "2",
            "user_id": "user2",
            "event_type": "logout",
            "timestamp": "2023-01-01T12:30:00Z",
        },
    ]
    summary = {
        "total_events": len(audit_events),
        "event_types": {
            "login": sum(1 for event in audit_events if event["event_type"] == "login"),
            "logout": sum(
                1 for event in audit_events if event["event_type"] == "logout"
            ),
        },
    }
    with open("audit_summary.json", "w") as f:
        json.dump(summary, f)
    return summary


if __name__ == "__main__":
    print(summarize_audit_events())
