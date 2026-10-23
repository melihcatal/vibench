import json
from typing import List, Dict

from security_models import KeyUsageEvent

def generate_audit_note(events: List[KeyUsageEvent]) -> str:
    """Create a JSON‑encoded audit note that can be stored alongside ciphertext for semantic search.

    The note bundles key usage metadata and a short human‑readable summary.
    """
    note = {
        'audit_id': 'crypto-audit-2024',
        'generated_at': datetime.utcnow().isoformat() + 'Z',
        'summary': summarize_usage(events),  # re‑use helper from key_usage_summary.py (inline copy if needed)
        'details': [dict(e) for e in events]  # convert TypedDict to plain dict
    }
    return json.dumps(note, indent=2)

# Helper re‑implementation of summarize_usage to avoid import cycles (copy‑paste summary logic)
from datetime import datetime
import json

def _summarize_usage(events: List[KeyUsageEvent]) -> str:
    if not events:
        return \"No key usage events recorded.\"
    events.sort(key=lambda e: e['timestamp'])
    lines = ['Key Usage Summary ({} events):\n'.format(len(events))]
    for ev in events:
        ts = datetime.fromisoformat(ev['timestamp']).strftime('%Y-%m-%d %H:%M:%S UTC')
        ctx = json.dumps(ev['context'], separators=(',', ':'))
        lines.append(f"[{ts}] {ev['operation'].upper():<8} {ev['key_name']} [{ev['context'].get('resource','')}]")
    return \"\\n\".join(lines)

# For demonstration: simple CLI entry point
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Generate crypto audit embedding JSON.')
    parser.add_argument('json_events', help='Path to JSON file containing list of KeyUsageEvent entries.')
    args = parser.parse_args()
    with open(args.json_events, 'r') as f:
        events = json.load(f)
    print(generate_audit_note(events))
