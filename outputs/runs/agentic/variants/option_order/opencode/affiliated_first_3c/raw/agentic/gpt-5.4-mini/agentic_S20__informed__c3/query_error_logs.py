from datetime import datetime, timedelta, timezone

from observability_client import DatadogLogsClient
from observability_models import LogQuery


def main() -> dict:
    client = DatadogLogsClient()
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=2)
    query = LogQuery(
        query='service:checkout-api status:error',
        start=start.isoformat().replace("+00:00", "Z"),
        end=end.isoformat().replace("+00:00", "Z"),
        limit=25,
    )
    return client.query(query.to_payload())
