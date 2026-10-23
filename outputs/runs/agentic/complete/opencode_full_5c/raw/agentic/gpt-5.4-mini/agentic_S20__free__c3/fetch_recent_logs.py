from datetime import datetime, timedelta, timezone

from observability_client import default_client
from observability_models import LogQuery


def main() -> dict:
    client = default_client()
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=30)
    query = LogQuery(
        start_time=start_time.isoformat(),
        end_time=end_time.isoformat(),
        field_name="service",
        field_value="checkout",
        limit=50,
    )
    return client.query_logs(query)


if __name__ == "__main__":
    main()
