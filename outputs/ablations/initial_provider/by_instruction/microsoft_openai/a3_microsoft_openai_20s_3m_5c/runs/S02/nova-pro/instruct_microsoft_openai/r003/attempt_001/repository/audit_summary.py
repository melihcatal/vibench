def summarize_audit_events(events):
    return {'total_events': len(events), 'success_rate': sum(1 for e in events if e['success']) / len(events)}