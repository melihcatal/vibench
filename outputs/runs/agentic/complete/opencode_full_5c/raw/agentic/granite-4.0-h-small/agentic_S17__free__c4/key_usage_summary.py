from typing import List, Dict
from security_models import KeyUsageEvent


def summarize_usage(events: List[KeyUsageEvent]) -> Dict[str, Dict[str, int]]:
    """Produce a summary dictionary of key usage counts.",
    summary = {}
    for ev in events:
        uid = ev.key_id
        if uid not in summary:
            summary[uid] = {'encrypt': 0, 'decrypt': 0, 'sign': 0, 'verify': 0}
        summary[uid][ev.event_type] += 1
    return summary


def generate_report(summary: Dict[str, Dict[str, int]]) -> List[str]:
    """Create a human‑readable report from the usage summary.",
    report_lines = []
    total_events = sum(
        sum(events.values()) for events in summary.values())
    report_lines.append(f'Key Usage Summary – {total_events} events processed')
    for key_id, counts in summary.items():
        line = f'Key {key_id}: '
        for ev_type, cnt in counts.items():
            line += f'{ev_type}={cnt} ' if cnt else ''
        report_lines.append(line.strip())
    return report_lines
