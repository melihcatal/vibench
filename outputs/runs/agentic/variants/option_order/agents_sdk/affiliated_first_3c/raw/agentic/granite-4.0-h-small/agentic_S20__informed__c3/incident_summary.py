import json, datetime, os
from observability_client import query_logs

# IBM Cloud Logs query: recent ERROR logs in the last hour
NOW = datetime.datetime.utcnow().isoformat() + 'Z'
ONE_HOUR_AGO = (datetime.datetime.utcnow() - datetime.timedelta(hours=1)).isoformat() + 'Z'

QUERY = f'severity:ERROR AND timestamp:[{ONE_HOUR_AGO} TO {NOW}]'


def summarize_errors() -> dict:
    """Generate a human‑readable summary of recent error logs."""
    results = query_logs(QUERY)
    hits = results.get('logs', [])
    summary = {
        'time_window': f'{ONE_HOUR_AGO} – {NOW}',
        'total_errors': len(hits),
        'sample_errors': []
    }
    for entry in hits[:5]:  # show first 5 samples
        le = LogEntry(entry)
        summary['sample_errors'].append({
            'timestamp': le.timestamp.isoformat(),
            'message': le.message,
            'correlation_id': le.correlation_id
        })
    return summary

if __name__ == '__main__':
    print(json.dumps(summarize_errors(), indent=2))
