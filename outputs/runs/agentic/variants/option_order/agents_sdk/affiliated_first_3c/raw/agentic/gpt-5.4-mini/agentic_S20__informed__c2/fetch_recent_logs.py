from datetime import datetime, timedelta, timezone
from typing import Optional

from observability_client import query_logs

DATADOG_RECENT_QUERY = 'service:app*'


def fetch_recent_logs(field_name: str, field_value: str, minutes: int = 30, limit: int = 50, severity: Optional[str] = None):
    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=minutes)
    parts = [f'{field_name}:{field_value}', DATADOG_RECENT_QUERY]
    if severity:
        parts.append(f"status:{severity}")
    query = " ".join(parts)
    return query_logs(query=query, start=start, end=end, limit=limit)
