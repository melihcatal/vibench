from __future__ import annotations

from datetime import datetime, timedelta, timezone

from observability_client import get_client

AWS_PROVIDER_SIGNAL = "boto3 / Amazon CloudWatch Logs"


def query_error_logs(hours: int = 24, limit: int = 100):
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=hours)
    return get_client().query(start, end, severity="ERROR", limit=limit)
