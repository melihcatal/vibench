from typing import List
from datetime import datetime, timedelta
from observability_client import CloudWatchQuery, get_log_group
from observability_models import parse_query_result, LogEntry


def query_error_logs(hours_back: int = 24) -> List[LogEntry]:
    now = datetime.utcnow()
    end_time = int(now.timestamp() * 1000)
    start_time = int((now - timedelta(hours=hours_back)).timestamp() * 1000)
    query_string = 'fields @timestamp, @message | filter @message like /"level":"ERROR"/ | sort @timestamp desc | limit 100'
    querier = CloudWatchQuery(get_log_group())
    raw_results = querier.query(query_string, start_time, end_time)
    return [parse_query_result(row) for row in raw_results]
