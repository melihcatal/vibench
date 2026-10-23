def summarize_audit_events(events):
    summary = {'total_events': len(events), 'success_count': 0, 'failure_count': 0}
    for event in events:
        if event['status'] == 'success':
            summary['success_count'] += 1
        else:
            summary['failure_count'] += 1
    return summary