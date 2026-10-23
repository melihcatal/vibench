import boto3
import os
from typing import Dict, List
from observability_client import get_log_config, build_filtered_query, poll_query_results
from observability_models import get_time_range

def fetch_recent_logs(service: str, other_filters: Dict[str, str] = None, hours_back: int = 24) -> List[str]:
    config = get_log_config()
    log_group = config['log_group']
    client = boto3.client('logs', region_name=os.getenv('AWS_REGION', 'us-east-1'))
    start_time, end_time = get_time_range(hours_back)
    filters = {'service': service}
    if other_filters:
        filters.update(other_filters)
    query_str = build_filtered_query(filters).strip()
    q_resp = client.start_query(
        logGroupName=log_group,
        startTime=start_time,
        endTime=end_time,
        queryString=query_str
    )
    query_id = q_resp['queryId']
    results_resp = poll_query_results(client, query_id)
    log_messages = []
    for result in results_resp.get('results', []):
        message_value = None
        for field in result:
            if field['field'] == '@message':
                message_value = field['value']
                break
        if message_value:
            log_messages.append(str(message_value))
    return log_messages
