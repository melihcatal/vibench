from __future__ import annotations

from observability_client import query_recent_logs

AWS_PROVIDER_SIGNAL = "boto3 / Amazon CloudWatch Logs"


def fetch_recent_logs(hours: int = 1, **field_filters):
    return query_recent_logs(hours=hours, **field_filters)
