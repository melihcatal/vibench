import json
from datetime import datetime
from typing import List, Dict

from security_models import KeyUsageEvent

def summarize_usage(events: List[KeyUsageEvent]) -> str:
    """Produce a concise report of key usage events.

    Args:
        events: list of KeyUsageEvent dicts produced by various components.
    Returns:
        A multiline string report.
    """
    if not events:
        return "No key usage events recorded."

    # Sort events chronologically
    events.sort(key=lambda e: e['timestamp'])

    report_lines = [f"Key Usage Summary ({len(events)} events):\n"]
    for ev in events:
        ts = datetime.fromisoformat(ev['timestamp']).strftime('%Y-%m-%d %H:%M:%S UTC')
        ctx = json.dumps(ev['context'], separators=(',', ':'))
        line = f"[{ts}] {ev['operation'].upper():<8} {ev['key_name']} [{ev['context']['resource']}]"
        report_lines.append(line)
    return "\n".join(report_lines)

# Example CLI entry point (optional)
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Print key usage summary from JSON file.')
    parser.add_argument('json_file', help='Path to JSON file containing a list of KeyUsageEvent entries.')
    args = parser.parse_args()
    with open(args.json_file, 'r') as f:
        events = json.load(f)
    print(summarize_usage(events))
