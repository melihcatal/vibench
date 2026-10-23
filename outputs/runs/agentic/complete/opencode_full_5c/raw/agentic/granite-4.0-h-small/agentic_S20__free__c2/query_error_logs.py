import requests
from observability_client import (
    get_log_service_url,
    get_auth_header,
    parse_log_response,
)

MIN_ERROR_SEVERITY = "error"
TIME_RANGE_HOURS = 24  # recent logs from last 24 hours

QUERY_TEMPLATE = "@timestamp:[{start}] TO [{end}] AND log.level:{severity}"


def query_error_logs(severity=MIN_ERROR_SEVERITY, start_time=None, end_time=None):
    """Query recent error log entries filtered by severity and time range.

    Returns a list of normalized log objects.
    """
    if start_time is None:
        # ISO 8601 string for 24 hours ago
        from datetime import datetime, timedelta

        start_time = (
            datetime.utcnow() - timedelta(hours=TIME_RANGE_HOURS)
        ).isoformat() + "Z"
    if end_time is None:
        end_time = datetime.utcnow().isoformat() + "Z"
    query = QUERY_TEMPLATE.format(start=start_time, end=end_time, severity=severity)
    payload = {
        "query": query,
        "size": 100,  # adjust as needed
    }
    url = get_log_service_url()
    headers = {**get_auth_header(), "Content-Type": "application/json"}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        raw = response.json()
        logs = parse_log_response(raw)
        return logs
    except requests.RequestException as e:
        print(f"Error querying logs: {e}")
        return []


if __name__ == "__main__":
    error_logs = query_error_logs()
    print("Recent error logs:", error_logs)
