from typing import List
from identity_models import AuditEvent

def summarize_audit(events: List[AuditEvent]) -> dict:
    summary = {
        'total_events': len(events),
        'unique_users': len({e.user_id for e in events}),
        'providers': {},
        'event_counts': {}
    }
    for ev in events:
        summary['providers'][ev.provider] = summary['providers'].get(ev.provider, 0) + 1
        summary['event_counts'][ev.event_type] = summary['event_counts'].get(ev.event_type, 0) + 1
    return summary

if __name__ == '__main__':
    # Demo with synthetic events
    events = [
        AuditEvent(event_id='1', timestamp='2023-01-01T12:00', user_id='u1', provider='Auth0', event_type='login'),
        AuditEvent(event_id='2', timestamp='2023-01-01T12:05', user_id='u1', provider='Auth0', event_type='callback'),
        AuditEvent(event_id='3', timestamp='2023-01-01T12:10', user_id='u2', provider='AzureAD', event_type='login')
    ]
    print('Audit summary:', summarize_audit(events))
