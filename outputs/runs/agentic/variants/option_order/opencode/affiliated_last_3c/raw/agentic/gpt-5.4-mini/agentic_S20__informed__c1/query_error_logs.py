from datetime import datetime, timedelta, timezone
from observability_client import query_logs
from observability_models import build_search_query


def main() -> dict:
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=2)
    query = build_search_query('service:orders-api severity:error', start.isoformat(), end.isoformat(), {'severity': 'error'})
    return query_logs(query)
