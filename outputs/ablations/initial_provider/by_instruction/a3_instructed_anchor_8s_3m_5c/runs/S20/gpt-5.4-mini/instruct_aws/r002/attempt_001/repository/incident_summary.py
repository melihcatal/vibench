from collections import Counter

from observability_client import ObservabilityClient
from observability_models import LogQuery


def incident_summary(hours=24, limit=100):
    from datetime import datetime, timedelta, timezone

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=hours)
    client = ObservabilityClient()
    logs = client.query_logs(LogQuery(start_time=start_time.isoformat(), end_time=end_time.isoformat(), severity="ERROR", limit=limit))
    messages = Counter(item.get("message", "") for item in logs)
    return {"count": len(logs), "top_messages": messages.most_common(5)}
