from observability_client import get_logging_client
from datetime import datetime, timedelta


def query_error_logs(
    project_id: str, severity: str = "ERROR", time_range_minutes: int = 60
) -> list[dict]:
    client = get_logging_client()
    now = datetime.utcnow()
    time_filter = now - timedelta(minutes=time_range_minutes)
    query = f'severity=("{severity}" OR "CRITICAL" OR "ALERT" OR "EMERGENCY") AND timestamp>="{time_filter.isoformat()}Z"'

    entries = client.list_entries(
        filter_=query, order_by="timestamp desc", project_ids=[project_id]
    )

    results = []
    for entry in entries:
        payload = entry.payload
        if isinstance(payload, dict):
            results.append(payload)
        elif isinstance(payload, str):
            results.append({"message": payload, "severity": entry.severity})
    return results
