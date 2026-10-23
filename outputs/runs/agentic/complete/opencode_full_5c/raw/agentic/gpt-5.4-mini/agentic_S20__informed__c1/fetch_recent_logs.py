from datetime import datetime, timedelta, timezone

from observability_client import client_from_env
from observability_models import QueryWindow


def fetch_recent_logs(field_filters=None, minutes: int = 60):
    client = client_from_env()
    end_time = datetime.now(timezone.utc)
    window = QueryWindow(
        start_time=end_time - timedelta(minutes=minutes), end_time=end_time
    )
    return client.recent(field_filters=field_filters, window=window)
