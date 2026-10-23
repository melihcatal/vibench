import boto3
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from observability_client import CLOUDWATCH_LOG_GROUP, execute_query
from observability_models import parse_query_row

def fetch_recent_logs(service: Optional[str] = None, correlation_id: Optional[str] = None, hours_back: int = 24) -> List[Dict[str, str]]:
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=hours_back)
    start_sec = int(start_time.timestamp())
    end_sec = int(end_time.timestamp())
    
    filter_parts = []
    if service:
        filter_parts.append(f'service = "{service}"')
    if correlation_id:
        filter_parts.append(f'corr_id = "{correlation_id}"')
    filter_clause = ' and '.join(filter_parts) if filter_parts else 'true'
    
    query_string = f'''
fields @timestamp, @message
| parse @message '*"level":"*","message":"*","service":"*","correlation_id":"*"*' as level, msg, service, corr_id
| filter {filter_clause}
| sort @timestamp desc
| limit 100
    '''
    
    client = boto3.client('logs', region_name=os.getenv('AWS_REGION', 'us-east-1'))
    results = execute_query(client, CLOUDWATCH_LOG_GROUP, start_sec, end_sec, query_string)
    logs = [parse_query_row(row) for row in results]
    return logs
