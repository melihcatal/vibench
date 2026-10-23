import json
from typing import List, Dict
from observability_models import LogRecord, CorrelatedLogBatch
from observability_client import get_log_client, put_log

# Re-use Simple Log Service client logic from the same-scenario imports (aliyun.log)
from aliyun.log import LogClient, LogItem

# Assume the client object is already configured in same-scenario files
# For this later-step file we import it locally if needed
sla_client = get_log_client()  # type: ignore


def summarize_error_incident(logs: List[LogRecord], window_minutes: int = 30) -> Dict[str, any]:
    """Summarize error-log findings for incident review.

    :param logs: List of LogRecord dictionaries returned from query_error_logs or fetch_recent_logs.
    :param window_minutes: Time window considered for the summary (default 30).
    :return: A dictionary containing counts, representative messages, and top error signatures.
    """
    # Filter only error entries that occurred within the recent window
    now = datetime.datetime.utcnow()
    start = now - datetime.timedelta(minutes=window_minutes)
    error_logs = [
        rec for rec in logs
        if rec['__severity__'].upper() == 'ERROR' and start.isoformat() + 'Z' <= rec['__time__'] <= now.isoformat() + 'Z'
    ]
    summary = {
        'total_error_count': len(error_logs),
        'sample_messages': [json.loads(rec['content'])['message'] for rec in error_logs[:5]],
        'top_error_signatures': []
    }
    # Simple signature extraction: module + exception type (naive string parse)
    signatures = {}
    for rec in error_logs:
        try:
            payload = json.loads(rec['content'])
            module = payload.get('module', 'unknown')
            exc = payload.get('exception', 'unknown')
            sig = f'{module}.{exc}'
            signatures[sig] = signatures.get(sig, 0) + 1
        except Exception:
            continue
    top_sigs = sorted(signatures.items(), key=lambda kv: kv[1], reverse=True)[:3]
    summary['top_error_signatures'] = [sig for sig, cnt in top_sigs]
    return summary
