import os
from datetime import datetime, timedelta
import json

import boto3

def rotation_summary(secret_arn: str, look_back_days: int = 7) -> dict:
    client = boto3.client("logs", region_name=os.environ.get("AWS_REGION", "us-east-1"))

    end_time = datetime.now()
    start_time = end_time - timedelta(days=look_back_days)

    # CloudWatch Logs group for Secrets Manager rotation events
    log_group_name = "/aws/secretsmanager"

    query = f"fields @timestamp, @message | filter secretArn = '{secret_arn}' | filter @message like /successfully rotated/ | sort @timestamp desc"

    start_query_response = client.start_query(
        logGroupName=log_group_name,
        startTime=int(start_time.timestamp() * 1000),
        endTime=int(end_time.timestamp() * 1000),
        queryString=query,
        limit=100
    )

    query_id = start_query_response['queryId']

    response = None
    while response is None or response['status'] == 'Running' or response['status'] == 'Scheduled':
        import time
        time.sleep(1) # Wait a bit for query to complete
        response = client.get_query_results(queryId=query_id)

    rotation_events = []
    for row in response['results']:
        event = {}
        for field in row:
            event[field['field']] = field['value']
        rotation_events.append(event)

    return {"secret_arn": secret_arn, "rotation_events": rotation_events, "summary_period_days": look_back_days}
