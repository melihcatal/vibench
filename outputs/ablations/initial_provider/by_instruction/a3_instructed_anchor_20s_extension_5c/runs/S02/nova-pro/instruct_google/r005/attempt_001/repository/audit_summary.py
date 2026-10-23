import json

def summarize_audit_events(audit_events):
    summarized_events = {
        'total_events': len(audit_events),
        'successful_logins': sum(1 for event in audit_events if event['status'] == 'success'),
        'failed_logins': sum(1 for event in audit_events if event['status'] == 'failure')
    }
    return summarized_events

if __name__ == '__main__':
    audit_events = [
        {'status': 'success', 'timestamp': '2022-01-01T12:00:00Z'},
        {'status': 'failure', 'timestamp': '2022-01-01T12:01:00Z'},
        {'status': 'success', 'timestamp': '2022-01-01T12:02:00Z'}
    ]
    summary = summarize_audit_events(audit_events)
    print(json.dumps(summary, indent=2))