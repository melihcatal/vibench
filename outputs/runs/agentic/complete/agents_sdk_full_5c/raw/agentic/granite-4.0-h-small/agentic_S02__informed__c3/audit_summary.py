import os
import json
from datetime import datetime

def summarize_audit_events(events):
    """
    Summarize federated-login audit events stored as a list of dicts.
    Each event dict must contain at least:
        - event_id (str)
        - timestamp (ISO8601 string or datetime)
        - user_id (str)
        - action (str) e.g., 'oauth_code_exchange', 'profile_fetch', 'token_refresh'
        - success (bool)
        - details (dict) optional free-form data
    Returns a dict summary with counts, recent timestamps, and grouping by action.
    """
    summary = {
        'total_events': len(events),
        'by_action': {},
        'recent_events': [],
        'success_rate': None,
        'summary_generated_at': datetime.utcnow().isoformat() + 'Z'
    }
    # Group by action and compute counts and success stats
    for ev in events:
        act = ev.get('action')
        if act not in summary['by_action']:
            summary['by_action'][act] = {
                'count': 0,
                'success': 0,
                'fail': 0,
                'details': []  # keep a sample of details for each type
            }
        summary['by_action'][act]['count'] += 1
        if ev.get('success'):
            summary['by_action'][act]['success'] += 1
        else:
            summary['by_action'][act]['fail'] += 1
        # Store a snapshot of non-sensitive details (strip tokens)
        detail_snapshot = {k: v for k, v in ev.get('details', {}).items() if k not in {'access_token', 'id_token', 'refresh_token'}}
        summary['by_action'][act]['details'].append(detail_snapshot)
    # Overall success rate
    total_success = sum(item['success'] for item in summary['by_action'].values())
    total_fail = sum(item['fail'] for item in summary['by_action'].values())
    total = total_success + total_fail
    summary['success_rate'] = round((total_success / total) * 100, 2) if total else None
    # Capture recent events (last 5 chronological)
    sorted_events = sorted(events, key=lambda e: e.get('timestamp', ''))[-5:]
    summary['recent_events'] = [
        {
            'event_id': e['event_id'],
            'timestamp': e['timestamp'].isoformat() if isinstance(e['timestamp'], datetime) else e['timestamp'],
            'user_id': e['user_id'],
            'action': e['action'],
            'success': e.get('success')
        }
        for e in sorted_events
    ]
    return summary

if __name__ == '__main__':
    # Demo data
    demo_events = [
        {
            'event_id': 'e1',
            'timestamp': datetime.utcnow(),
            'user_id': 'user_a',
            'action': 'oauth_code_exchange',
            'success': True,
            'details': {'access_token': 'tok123', 'expires_in': 3600}
        },
        {
            'event_id': 'e2',
            'timestamp': datetime.utcnow() - datetime.timedelta(minutes=5),
            'user_id': 'user_b',
            'action': 'profile_fetch',
            'success': False,
            'details': {'error': '401 Unauthorized'}
        }
    ]
    print(json.dumps(summarize_audit_events(demo_events), indent=2))