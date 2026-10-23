def summarize_audit_events(events):
    summaries = []
    for event in events:
        summaries.append(f"User {event['user_id']} logged in at {event['timestamp']}")
    return summaries
