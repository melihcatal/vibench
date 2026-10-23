def summarize_audit_events(events):
    summary = {'total': len(events), 'success': 0, 'failure': 0}
    for event in events:
        if event['status'] == 'success':
            summary['success'] += 1
        else:
            summary['failure'] += 1
    return summary