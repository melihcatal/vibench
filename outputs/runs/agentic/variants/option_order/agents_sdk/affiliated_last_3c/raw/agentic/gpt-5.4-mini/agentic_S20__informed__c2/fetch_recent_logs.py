from __future__ import annotations

from datetime import datetime, timedelta, timezone

from observability_client import get_client
from observability_models import LogQuery

SERVICE = "Google Cloud Logging"
MODEL_OR_SERVICE_SIGNAL = "google.cloud.logging"


def fetch_recent_logs(field_name: str = "service", field_value: str = "checkout", minutes: int = 30) -> dict:
    now = datetime.now(timezone.utc)
    query = LogQuery(
        start_time=now - timedelta(minutes=minutes),
        end_time=now,
        field_filters={field_name: field_value},
        limit=100,
    )
    return get_client().query_logs(query).to_dict()
