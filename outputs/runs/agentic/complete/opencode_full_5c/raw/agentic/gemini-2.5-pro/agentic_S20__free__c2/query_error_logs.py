from datetime import datetime, timedelta, timezone
from observability_client import get_logging_client
from observability_models import LOG_NAME


def query_recent_errors():
    logging_client = get_logging_client()

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=1)

    time_filter = f'timestamp >= "{start_time.isoformat()}" AND timestamp <= "{end_time.isoformat()}"'

    severity_filter = 'severity="ERROR"'
    log_name_filter = f'logName="projects/{logging_client.project}/logs/{LOG_NAME}"'

    combined_filter = f"{log_name_filter} AND {severity_filter} AND {time_filter}"

    entries = logging_client.list_entries(
        filter_=combined_filter, order_by=logging_client.DESCENDING
    )

    for entry in entries:
        print(f"Timestamp: {entry.timestamp}, Payload: {entry.payload}")


if __name__ == "__main__":
    query_recent_errors()
