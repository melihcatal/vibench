import time
import json
from typing import List, Dict, Any
from observability_client import ObservabilityClient
from observability_models import LogQueryResult

def fetch_recent_logs(log_group_names: List[str], start_time_seconds: int, end_time_seconds: int, filters: Dict[str, str]) -> LogQueryResult:
    client = ObservabilityClient()

    filter_parts = []
    for field, value in filters.items():
        # Assuming JSON messages where fields are nested, e.g., 'message.some_field'
        filter_parts.append(f'json_extract(@message, \'$.{field}\') = \"{value}\'')
    
    filter_string = " and ".join(filter_parts)
    
    query_string = f"fields @timestamp, @message | filter {filter_string} | sort @timestamp desc"

    query_id = client.start_query(
        log_group_names=log_group_names,
        start_time=start_time_seconds,
        end_time=end_time_seconds,
        query_string=query_string
    )

    status = 'Running'
    while status in ['Running', 'Scheduled']:
        time.sleep(1)
        results = client.get_query_results(query_id)
        status = results['status']

    if status == 'Complete':
        return LogQueryResult.from_aws_cloudwatch_insights_response(results)
    else:
        raise Exception(f"CloudWatch Logs Insights query failed with status: {status}")
