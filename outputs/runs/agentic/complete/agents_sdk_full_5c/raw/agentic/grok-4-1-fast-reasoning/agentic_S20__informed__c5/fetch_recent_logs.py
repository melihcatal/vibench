import time
from typing import List, Dict, Any
from observability_client import run_log_query
from observability_models import build_recent_logs_query

def fetch_recent_logs(filter_pattern: str = 'error', hours_ago: int = 1) -> List[Dict[str, Any]]:
    """
    Retrieves recent log results filtered by field values and time range from Amazon CloudWatch Logs.
    """
    end_time = int(time.time() * 1000)
    start_time = end_time - (hours_ago * 60 * 60 * 1000)
    query_string = build_recent_logs_query(filter_pattern, start_time, end_time)
    return run_log_query(start_time, end_time, query_string)
