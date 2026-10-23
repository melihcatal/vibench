from datetime import datetime, timedelta, timezone
from observability_client import get_logging_client
from observability_models import LOG_NAME


def fetch_logs_by_field():
    logging_client = get_logging_client()

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=1)

    time_filter = f'timestamp >= "{start_time.isoformat()}" AND timestamp <= "{end_time.isoformat()}"'

    field_filter = 'jsonPayload.user_id="user12345"'
    log_name_filter = f'logName="projects/{logging_client.project}/logs/{LOG_NAME}"'

    combined_filter = f"{log_name_filter} AND {field_filter} AND {time_filter}"

    entries = logging_client.list_entries(filter_=combined_filter)

    for entry in entries:
        print(f"Found log for user_id: user12345, Payload: {entry.payload}")


if __name__ == "__main__":
    fetch_logs_by_field()
