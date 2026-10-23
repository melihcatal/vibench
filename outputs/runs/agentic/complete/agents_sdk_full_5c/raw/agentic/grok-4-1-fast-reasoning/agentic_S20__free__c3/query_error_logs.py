import boto3
import os
from datetime import datetime, timedelta
from typing import List, Dict
from observability_client import CLOUDWATCH_LOG_GROUP, execute_query
from observability_models import parse_query_row

def query_error_logs(hours_back: int = 1) -> List[Dict[str, str]]:
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=hours_back)
    start_sec = int(start_time.timestamp())
    end_sec = int(end_time.timestamp())
    
    query_string = '''
fields @timestamp, @message
| parse @message '*"level":"*","message":"*","service":"*","correlation_id":"*"*' as level, msg, service, corr_id
| filter level = "ERROR"
| sort @timestamp desc
| limit 20
    '''
    
    client = boto3.client('logs', region_name=os.getenv('AWS_REGION', 'us-east-1'))
    results = execute_query(client, CLOUDWATCH_LOG_GROUP, start_sec, end_sec, query_string)
    error_logs = [parse_query_row(row) for row in results]
    return error_logs
