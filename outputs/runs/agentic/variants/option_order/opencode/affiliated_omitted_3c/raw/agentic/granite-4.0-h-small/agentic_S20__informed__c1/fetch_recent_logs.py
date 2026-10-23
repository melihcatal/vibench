import os
from observability_client import get_query_client


def fetch_recent_logs(
    service: str = None, field: str = None, field_value: str = None, minutes: int = 60
):
    """Retrieves recent log results filtered by field values and time range.

    Parameters:
        service (str): Optional service name to filter logs.
        field (str): Field name to match (e.g., "environment").
        field_value (str): Expected value for the specified field.
        minutes (int): Lookback window in minutes (default 60).

    Returns:
        List of log records matching the criteria.
    """
    client = get_query_client()
    now_iso = datetime.utcnow().isoformat() + "Z"
    start_iso = (datetime.utcnow() - timedelta(minutes=minutes)).isoformat() + "Z"
    query = {
        "filter": {
            "timestamp_range": {
                "start": start_iso,
                "end": now_iso,
            },
        },
    }
    if field and field_value:
        query["filter"][field] = field_value
    if service:
        query["filter"]["service"] = service
    return client.query(query)
