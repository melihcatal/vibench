import time
from typing import List, Dict, Any
from observability_client import run_log_query
from observability_models import build_error_query

def query_error_logs(severity: str = 'ERROR', hours_ago: int = 1) -> List[Dict[str, Any]]:
    """
    Queries recent error log entries filtered by severity and time range from Amazon CloudWatch Logs.
    """
    end_time = int(time.time() * 1000)
    start_time = end_time - (hours_ago * 60 * 60 * 1000)
    query_string = build_error_query(severity, start_time, end_time)
    return run_log_query(start_time, end_time, query_string)
