from datetime import datetime, timedelta, timezone
from observability_client import get_logs_client, resolve_log_name
from observability_models import build_query_request


def main():
    client = get_logs_client()
    log_name = resolve_log_name()
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=24)
    request = build_query_request(
        log_name=log_name,
        severity="ERROR",
        start_time=start_time,
        end_time=end_time,
        field_filters={"severity": "ERROR"},
    )
    client.query_error_logs(request)


if __name__ == "__main__":
    main()
