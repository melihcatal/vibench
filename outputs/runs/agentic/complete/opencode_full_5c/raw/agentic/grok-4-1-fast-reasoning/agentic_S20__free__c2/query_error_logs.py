from observability_client import ObservabilityClient
from datetime import datetime, timedelta
from typing import List, Dict, Any


def query_error_logs(hours_back: int = 1) -> List[Dict[str, Any]]:
    client = ObservabilityClient()
    now = datetime.utcnow()
    to_ts = int(now.timestamp() * 1000)
    from_ts = int((now - timedelta(hours=hours_back)).timestamp() * 1000)
    query = "status:error"
    logs = client.query_logs(query, from_ts, to_ts, limit=50)
    return logs
