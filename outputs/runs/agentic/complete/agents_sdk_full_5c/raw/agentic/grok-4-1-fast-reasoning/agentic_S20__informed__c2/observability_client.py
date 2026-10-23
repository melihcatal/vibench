import time
import os
from typing import Dict, Any

def get_log_config() -> Dict[str, Any]:
    return {
        'log_group': os.getenv('CLOUDWATCH_LOG_GROUP', 'observability-demo'),
        'structured_stream': 'structured-logs',
        'correlated_stream': 'correlated-logs'
    }

def build_error_query() -> str:
    return '''
fields @timestamp, @message | filter level == "ERROR" | sort @timestamp desc | limit 50
    '''

def build_filtered_query(filters: Dict[str, str]) -> str:
    filter_conditions = [f'{k} == "{v}"' for k, v in filters.items()]
    filter_str = ' AND '.join(filter_conditions)
    return f'''
fields @timestamp, @message | filter {filter_str} | sort @timestamp desc | limit 100
    '''

def poll_query_results(client: Any, query_id: str, poll_interval: float = 1.0, max_wait: int = 60) -> Dict[str, Any]:
    start_time = time.time()
    while time.time() - start_time < max_wait:
        response = client.describe_queries(queryIds=[query_id])
        query_status = response['queries'][0]
        status = query_status['status']
        if status == 'Complete':
            return client.get_query_results(queryId=query_id)
        if status == 'Failed':
            raise RuntimeError(f"Query {query_id} failed: {query_status.get('errorMessage', 'Unknown error')}")
        time.sleep(poll_interval)
    raise TimeoutError(f"Query {query_id} timed out after {max_wait}s")
