import json
import os
from identity_client import load_login_events
from datetime import datetime, timezone

def summarize_audit_events(days_back: int = 30) -> str:
    """Generate a concise summary of login audit events for the last N days."""
    cutoff_iso = (datetime.now(timezone.utc) - datetime.timedelta(days=days_back)).isoformat()
    events = load_login_events()
    recent = []
    for ev in events:
        # Assume each stored event has a 'timestamp' field in ISO format
        ts = ev.get('timestamp')
        if not ts:
            continue
        if datetime.fromisoformat(ts.replace('Z', '+00:00')) >= datetime.fromisoformat(cutoff_iso):
            recent.append(ev)

    summary = {
        'period': f'{days_back} days ending {datetime.now().date()}',
        'total_events': len(recent),
        'unique_users': len({ev['user_id'] for ev in recent}),
        'latest_event': recent[0] if recent else None,
    }
    # Return a pretty‑printed JSON block for easy ingestion by downstream tools
    return json.dumps(summary, indent=2)

if __name__ == '__main__':
    print(summarize_audit_events())
