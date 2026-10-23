import json
from datetime import datetime, timezone
type LogRecord = Dict[str, Any]

from observability_client import get_dd_api_key
from observability_models import LogRecord

def summarize_recent_errors(limit: int = 50, minutes_back: int = 30):
    """Retrieve recent error logs from Datadog and create a concise incident summary.",
    Returns a plain‑text summary string that can be forwarded to on‑call owners.",
    Raises:
        RuntimeError if the API request fails.",
    """
    api_key = get_dd_api_key()
    now = datetime.now(timezone.utc)
    start = (now - datetime.timedelta(minutes=minutes_back)).isoformat()
    endpoint = "https://http-intake.logs.datadoghq.com/v1/input"
    # Note: Datadog Logs API does not support a direct query endpoint.
    # We use the Logs Search endpoint instead.
    search_url = f"https://api.datadoghq.com/api/v2/logs-search?api_key={api_key}&application_key={api_key}"
    payload = {
        "query": f"service:app AND status:error AND @timestamp:[{start} TO *]",
        "start": int(now.timestamp()),
        "size": limit,
        "sort": "@timestamp:desc"
    }
    headers = {
        "Content-Type": "application/json",
        "DD-API-KEY": api_key
    }
    resp = requests.post(search_url, headers=headers, json=payload)
    resp.raise_for_status()
    data = resp.json()
    errors = data.get('logs', [])
    if not errors:
        return "No error logs found in the last {} minutes.".format(minutes_back)
    summary_lines = ["Incident Summary (last {} minutes):".format(minutes_back)]
    summary_lines.append(f"Found {len(errors)} error(s).")
    for rec in errors[:limit]:
        lr = LogRecord(**rec)
        summary_lines.append(f"{lr.timestamp} | {lr.severity} | {lr.correlation_id or 'N/A'} | {lr.message}")
    return \"\\n\".join(summary_lines)
