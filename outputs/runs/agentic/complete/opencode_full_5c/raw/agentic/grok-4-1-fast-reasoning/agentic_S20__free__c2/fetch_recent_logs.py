from observability_client import ObservabilityClient
from datetime import datetime, timedelta
from typing import List, Dict, Any


def fetch_recent_logs(
    filter_field: str, filter_value: str, hours_back: int = 24
) -> List[Dict[str, Any]]:
    client = ObservabilityClient()
    now = datetime.utcnow()
    to_ts = int(now.timestamp() * 1000)
    from_ts = int((now - timedelta(hours=hours_back)).timestamp() * 1000)
    query = f'{filter_field}:"{filter_value}"'
    logs = client.query_logs(query, from_ts, to_ts, limit=100)
    return logs
