import os
from datetime import datetime
from typing import Dict
from dotenv import load_dotenv

load_dotenv()

AUDIT_EVENTS = []


def add_event(event_type: str, details: Dict[str, Any] = {}):
    """Add an audit log entry (in-memory for demonstration)."""
    entry = {
        'event_id': str(uuid.uuid4()),
        'event_type': event_type,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'details': details
    }
    AUDIT_EVENTS.append(entry)
    print(f'Logged {event_type}: {entry["event_id"]}')


def summary() -> Dict:
    """Create a concise summary of the collected audit events."""
    summary = {'total_events': len(AUDIT_EVENTS)}
    type_counts = {}
    for ev in AUDIT_EVENTS:
        tp = ev['event_type']
        type_counts[tp] = type_counts.get(tp, 0) + 1
    summary['event_counts'] = type_counts
    latest = max(AUDIT_EVENTS, key=lambda ev: ev['timestamp'])
    summary['latest_event'] = latest
    return summary

# Example usage (for demo purposes)
if __name__ == '__main__':
    add_event('login', {'user_id': '123'})
    add_event('token_exchange', {'user_id': '123'})
    print('Audit summary:', summary())

# End of audit_summary.py