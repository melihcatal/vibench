from typing import List
from datetime import datetime, timedelta
from observability_client import CloudWatchQuery, get_log_group
from observability_models import parse_query_result, LogEntry


def fetch_recent_logs(
    filter_field: str, filter_value: str, minutes_back: int = 60
) -> List[LogEntry]:
    now = datetime.utcnow()
    end_time = int(now.timestamp() * 1000)
    start_time = int((now - timedelta(minutes=minutes_back)).timestamp() * 1000)
    query_string = f'fields @timestamp, @message | filter @message like /"{filter_field}":"{filter_value}"/ | sort @timestamp desc | limit 200'
    querier = CloudWatchQuery(get_log_group())
    raw_results = querier.query(query_string, start_time, end_time)
    return [parse_query_result(row) for row in raw_results]
