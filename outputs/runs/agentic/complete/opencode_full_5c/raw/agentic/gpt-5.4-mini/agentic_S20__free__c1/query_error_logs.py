from datetime import datetime, timedelta, timezone

from observability_client import query_logs
from observability_models import LogQueryRequest


def main() -> dict:
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=2)
    request = LogQueryRequest(
        start_time=start_time.isoformat(),
        end_time=end_time.isoformat(),
        severity="ERROR",
        field_filters={"service": "checkout-api"},
        limit=25,
    )
    return query_logs(request, log_name="application")


if __name__ == "__main__":
    main()
