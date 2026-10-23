import json
from datetime import datetime, timedelta
from observability_client import get_logger

def summarize_errors(minutes: int = 60) -> dict:
    """Summarizes recent error logs for an incident review.

    Collects counts per service (derived from log name), top error messages,
    and timestamps of first/last occurrences.
    """
    client = get_logger()  # Uses Cloud Logging client configured via env vars
    now = client.now()
    start = now - timedelta(minutes=minutes)
    query = f'logName:projects/my-project logs/my-log severity=ERROR timestamp>={start} timestamp<={now}'
    errors = list(client.logger('my-log').list_entries(filter_=query))
    summary = {
        'total_errors': len(errors),
        'first_timestamp': None,
        'last_timestamp': None,
        'error_counts': {},
        'sample_messages': []
    }
    if errors:
        summary['first_timestamp'] = errors[0].timestamp.isoformat()
        summary['last_timestamp'] = errors[-1].timestamp.isoformat()
        for entry in errors:
            payload = json.loads(entry.payload if isinstance(entry.payload, str) else entry.payload.decode('utf-8'))
            msg = payload.get('message', '')
            summary['error_counts'][msg] = summary['error_counts'].get(msg, 0) + 1
            summary['sample_messages'].append(msg)
    return summary

# Example usage (omit in library code)
if __name__ == '__main__':
    print(json.dumps(summarize_errors(120), indent=2))
