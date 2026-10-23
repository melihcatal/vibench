# Same-scenario implementation
from datetime import datetime, timedelta
from observability_client import get_logging_client

def fetch_recent_logs(field_filter="level:INFO", start_relative="30m"):
    """Retrieves recent log results filtered by field values and time range.

    Shows usage of the Loggly search API via the client in observability_client.
    The field_filter parameter can be any Lucene query (e.g., "user_id:123").
    Returns matching log entries as a list.
    """
    client = get_logging_client()
    end = datetime.utcnow()
    start = end - timedelta(seconds=parse_relative_duration(start_relative))
    query = f'{field_filter} AND timestamp:[{int(start.timestamp()) * 1000} TO {int(end.timestamp()) * 1000}]'
    return client.search_logs(query=query)}