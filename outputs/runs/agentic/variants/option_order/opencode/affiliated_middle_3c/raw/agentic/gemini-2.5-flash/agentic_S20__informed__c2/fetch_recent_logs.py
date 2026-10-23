from observability_client import get_logging_client
from datetime import datetime, timedelta


def fetch_recent_logs(
    project_id: str, log_name: str, time_range_minutes: int = 60, filters: dict = None
) -> list[dict]:
    client = get_logging_client()
    now = datetime.utcnow()
    time_filter = now - timedelta(minutes=time_range_minutes)

    query_parts = [
        f'logName="projects/{project_id}/logs/{log_name}"',
        f'timestamp>="{time_filter.isoformat()}Z"',
    ]

    if filters:
        for key, value in filters.items():
            query_parts.append(
                f'jsonPayload.{key}="{value}"'
            )  # Assuming structured logs and filtering on jsonPayload

    query = " AND ".join(query_parts)

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
