from datetime import datetime, timedelta, timezone

from observability_client import DatadogLogsClient
from observability_models import LogQuery


def main() -> dict:
    client = DatadogLogsClient()
    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=30)
    query = LogQuery(
        query='service:checkout-api environment:production',
        start=start.isoformat().replace("+00:00", "Z"),
        end=end.isoformat().replace("+00:00", "Z"),
        limit=50,
    )
    return client.query(query.to_payload())
