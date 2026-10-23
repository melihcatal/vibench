from datetime import datetime, timedelta, timezone

from observability_client import ObservabilityClient
from observability_models import LogQuery


def fetch_recent_logs(hours=1, limit=100, **field_filters):
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=hours)
    client = ObservabilityClient()
    query = LogQuery(
        start_time=start_time.isoformat(),
        end_time=end_time.isoformat(),
        field_filters=field_filters,
        limit=limit,
    )
    return client.query_logs(query)
