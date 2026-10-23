from datetime import datetime, timedelta, timezone
from observability_client import query_logs
from observability_models import build_search_query


def main() -> dict:
    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=30)
    query = build_search_query('service:orders-api status:info', start.isoformat(), end.isoformat(), {'service': 'orders-api', 'status': 'info'})
    return query_logs(query)
