import boto3
import time
from typing import List, Dict, Any
from observability_client import get_cloudwatch_config, build_field_filter_query, normalize_query_results
from observability_models import QueryResult

def fetch_recent_logs(field: str, value: str, duration_minutes: int = 60) -> QueryResult:
    config = get_cloudwatch_config()
    client = boto3.client('logs', region_name=config['region'])
    end_time = int(time.time() * 1000)
    start_time = end_time - (duration_minutes * 60 * 1000)
    query_string = build_field_filter_query(field, value)
    query_response = client.start_query(
        logGroupName=config['log_group'],
        logStreamNames=[config['log_stream']],
        startTime=start_time,
        endTime=end_time,
        queryString=query_string
    )
    query_id = query_response['queryId']
    while True:
        result_response = client.get_query_results(queryId=query_id)
        status = result_response['status']
        if status == 'Complete':
            return normalize_query_results(result_response.get('results', []))
        if status == 'Failed':
            raise RuntimeError(f"Query failed: {result_response.get('errorMessage', 'Unknown error')}")
        time.sleep(1)
