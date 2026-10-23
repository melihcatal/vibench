from observability_client import ObservabilityClient
from observability_models import LogQuery
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional


def fetch_recent_logs(
    time_range_minutes: int = 60,
    field_filters: Optional[Dict[str, str]] = None,
    severity: str = "INFO",  # Default to INFO severity
):
    client = ObservabilityClient()
    logging_client = client.get_logging_client()

    now = datetime.now(timezone.utc)
    start_time = now - timedelta(minutes=time_range_minutes)

    # Base filter for time range and severity
    filter_parts = [
        f'timestamp >= "{start_time.isoformat(timespec="seconds")}Z"',
        f'severity >= "{severity}"',
    ]

    # Add additional field filters
    if field_filters:
        for field, value in field_filters.items():
            filter_parts.append(
                f'{field} = "{value}"'
                if isinstance(value, str)
                else f"{field} = {value}"
            )

    filter_string = " AND ".join(filter_parts)
    print(f"Using filter: {filter_string}")

    log_query = LogQuery(filter_string=filter_string, order_by="timestamp desc")

    entries = logging_client.list_entries(
        filter_=log_query.filter_string,
        order_by=log_query.order_by,
        page_size=log_query.limit,
    )

    recent_logs = []
    for entry in entries:
        timestamp_dt = (
            entry.timestamp.isoformat(timespec="seconds") if entry.timestamp else "N/A"
        )

        log_data = {
            "timestamp": timestamp_dt,
            "severity": entry.severity,
            "log_name": entry.log_name,
            "resource_type": entry.resource.type if entry.resource else "N/A",
            "text_payload": entry.text_payload if entry.text_payload else None,
            "json_payload": entry.json_payload if entry.json_payload else None,
            "labels": entry.labels if entry.labels else None,
            "insert_id": entry.insert_id,
        }
        recent_logs.append(log_data)

    return recent_logs


if __name__ == "__main__":
    # Example usage: fetch recent INFO logs from the last 120 minutes with a specific label
    filters = {"labels.component": "auth"}
    recent_info_logs = fetch_recent_logs(
        time_range_minutes=120, field_filters=filters, severity="INFO"
    )
    if recent_info_logs:
        print(f"Found {len(recent_info_logs)} recent INFO logs:")
        for log in recent_info_logs:
            print(log)
    else:
        print("No INFO logs found with the specified filters in the time range.")
