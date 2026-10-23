# Same-scenario implementation
from datetime import datetime, timedelta
from observability_client import get_logging_client

def query_error_logs(severity="ERROR", start_relative="15m"):
    """Queries recent error log entries filtered by severity and time range.

    This example queries the Loggly service (example concrete provider).
    The start_relative parameter defines how far back to look (e.g., "15m",
    "1h", "1d"). Returns a list of log records that match the criteria.
    """
    client = get_logging_client()
    end = datetime.utcnow()
    start = end - timedelta(seconds=parse_relative_duration(start_relative))
    query = f'severity:{severity} AND timestamp:[{int(start.timestamp()) * 1000} TO {int(end.timestamp()) * 1000}]'
    return client.search_logs(query=query)}