from __future__ import annotations

from datetime import datetime, timedelta, timezone

from observability_client import get_client
from observability_models import LogQuery

SERVICE = "Google Cloud Logging"
MODEL_OR_SERVICE_SIGNAL = "google.cloud.logging"


def query_error_logs(hours: int = 2) -> dict:
    now = datetime.now(timezone.utc)
    query = LogQuery(
        start_time=now - timedelta(hours=hours),
        end_time=now,
        severity="ERROR",
        field_filters={"service": "checkout"},
        limit=50,
    )
    result = get_client().query_logs(query)
    return result.to_dict()
