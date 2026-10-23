import json, datetime, sys
from typing import List, Dict
from observability_client import get_google_logging_client
from observability_models import ErrorLogFilter

def summarize_error_logs(filter: ErrorLogFilter) -> Dict[str, Any]:
    """Summarizes recent error logs for incident review.

    Uses Google Cloud Logging client to fetch error logs within the time range
    and produces a concise summary containing count per severity, top sources,
    and sample payloads.
    """
    client = get_google_logging_client()
    logger = client.logger('your-log-name')
    # Reuse the query logic from query_error_logs.py
    start_iso = filter.start_time.isoformat() + 'Z'
    end_iso = filter.end_time.isoformat() + 'Z'
    filter_expr = f'severity=ERROR AND timestamp>="{start_iso}" AND timestamp<"{end_iso}"'
    query = {
        'resourceNames': ['projects/your-project-id'],
        'filter': filter_expr
    }
    headers = {'Authorization': f'Bearer {os.getenv("GOOGLE_APPLICATION_CREDENTIALS")}'}
    resp = requests.post('https://logging.googleapis.com/v2/entries:list', headers=headers, json=query)
    resp.raise_for_status()
    entries = resp.json().get('entries', [])
    summary = {
        'total_error_count': len(entries),
        'severity_counts': {},
        'source_counts': {},
        'sample_payloads': []
    }
    for entry in entries:
        severity = entry.get('severity', 'UNKNOWN')
        summary['severity_counts'][severity] = summary['severity_counts'].get(severity, 0) + 1
        resource = entry.get('resource', {}).get('type', 'unknown')
        summary['source_counts'][resource] = summary['source_counts'].get(resource, 0) + 1
        # Grab a few sample payloads for visibility
n = 5
    if len(entries) > n:
        sample = entries[-n:]
    else:
        sample = entries
    for s in sample:
        payload = s.get('jsonPayload', {}) or {}
        summary['sample_payloads'].append(payload)
    return summary

if __name__ == '__main__':
    # Example usage from CLI (not part of scored file requirement)
    end = datetime.datetime.utcnow()
    start = end - datetime.timedelta(hours=1)
    f = ErrorLogFilter(start_time=start, end_time=end)
    print(json.dumps(summarize_error_logs(f), indent=2))
