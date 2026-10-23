import json


# Summarize federated-login audit events
def summarize_audit_events(events):
    summarized_events = []
    for event in events:
        summarized_events.append(
            {
                "event_id": event.get("id"),
                "user_id": event.get("user_id"),
                "timestamp": event.get("timestamp"),
            }
        )
    return json.dumps(summarized_events, indent=2)
