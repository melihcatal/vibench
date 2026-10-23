import boto3
import os
from typing import List
from observability_client import get_log_config, build_error_query, poll_query_results
from observability_models import get_time_range

def query_error_logs(hours_back: int = 1) -> List[str]:
    config = get_log_config()
    log_group = config['log_group']
    client = boto3.client('logs', region_name=os.getenv('AWS_REGION', 'us-east-1'))
    start_time, end_time = get_time_range(hours_back)
    query_str = build_error_query().strip()
    q_resp = client.start_query(
        logGroupName=log_group,
        startTime=start_time,
        endTime=end_time,
        queryString=query_str
    )
    query_id = q_resp['queryId']
    results_resp = poll_query_results(client, query_id)
    error_messages = []
    for result in results_resp.get('results', []):
        message_value = None
        for field in result:
            if field['field'] == '@message':
                message_value = field['value']
                break
        if message_value:
            error_messages.append(str(message_value))
    return error_messages
