import json

def summarize_audit_events(audit_events):
    summary = {'total_events': len(audit_events), 'success_count': 0, 'failure_count': 0}
    for event in audit_events:
        if event['status'] == 'success':
            summary['success_count'] += 1
        else:
            summary['failure_count'] += 1
    return json.dumps(summary, indent=2)

if __name__ == '__main__':
    pass