def summarize_audit_events(events):
    summary = {}
    for event in events:
        if event['type'] not in summary:
            summary[event['type']] = 0
        summary[event['type']] += 1
    return summary