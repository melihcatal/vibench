def audit_summary(audit_events):
    summary = {
        'total_events': len(audit_events),
        'success_count': sum(1 for event in audit_events if event['status'] == 'success'),
        'failure_count': sum(1 for event in audit_events if event['status'] == 'failure')
    }
    return summary