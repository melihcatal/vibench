from datetime import datetime, timedelta, timezone

from observability_client import query_logs
from observability_models import QueryWindow


def main() -> None:
    window = QueryWindow(start_time=datetime.now(timezone.utc) - timedelta(hours=1), end_time=datetime.now(timezone.utc), severity="ERROR", field_filters={"service": "orders"})
    query_logs(window)


if __name__ == "__main__":
    main()
