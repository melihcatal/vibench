import json
import os
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class AuditEvent:
    event_id: str
    timestamp: str  # ISO8601
    user_sub: str
    event_type: str  # e.g., 'login', 'token_refresh', 'consent_granted'
    details: Dict[str, Any]
    source: str  # e.g., 'auth0', 'internal'

def load_audit_records(filepath: str = 'audit_log.json') -> List[AuditEvent]:
    """Load audit events from a JSON Lines file stored in a managed NoSQL store or file system."""
    path = os.getenv('AUDIT_STORE_PATH', filepath)
    events = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():  # skip empty lines
                    events.append(json.loads(line))
    except FileNotFoundError:
        # No audit log yet – start with empty list
        pass
    # Convert to typed objects
    return [AuditEvent(**e) for e in events]


def summarize_last_24h(events: List[AuditEvent]) -> Dict[str, Any]:
    """Produce a concise summary of login-related events in the last 24 hours."""
    from datetime import datetime, timezone, timedelta
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=1)
    recent = [e for e in events if datetime.fromisoformat(e.timestamp) >= cutoff]
    summary = {
        'total_events': len(recent),
        'logins': [],
        # simple count per event_type
        'event_counts': {},
    }
    for ev in recent:
        if ev.event_type == 'login':
            summary['logins'].append({'timestamp': ev.timestamp, 'details': ev.details})
        summary['event_counts'][ev.event_type] = summary['event_counts'].get(ev.event_type, 0) + 1
    return summary

# Example CLI usage (feel free to integrate elsewhere)
if __name__ == '__main__':
    events = load_audit_records()
    summary = summarize_last_24h(events)
    print(json.dumps(summary, indent=2))
