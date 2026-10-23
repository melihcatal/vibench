import json


def summarize_audit_events(audit_events):
    summary = {
        'total_events': len(audit_events),
        'successful_logins': sum(1 for event in audit_events if event['status'] == 'success'),
        'failed_logins': sum(1 for event in audit_events if event['status'] == 'failure')
    }
    return json.dumps(summary, indent=2)