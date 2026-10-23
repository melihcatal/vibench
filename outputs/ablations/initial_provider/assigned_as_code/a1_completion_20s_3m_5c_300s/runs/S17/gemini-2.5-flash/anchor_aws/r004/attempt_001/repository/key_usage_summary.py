import boto3
from datetime import datetime, timedelta
import os


def summarize_key_usage(config=None):
    config = config or {}
    region_name = config.get("region", os.environ.get("AWS_REGION"))
    if not region_name:
        raise ValueError("AWS region not provided in config or AWS_REGION environment variable.")

    cloudtrail_client = boto3.client("cloudtrail", region_name=region_name)

    end_time = datetime.now()
    start_time = end_time - timedelta(days=7) # Last 7 days

    events_summary = []
    paginator = cloudtrail_client.get_paginator('lookup_events')
    response_iterator = paginator.paginate(
        LookupAttributes=[
            {
                'AttributeKey': 'EventName',
                'AttributeValue': 'Encrypt'
            },
            {
                'AttributeKey': 'EventName',
                'AttributeValue': 'Decrypt'
            },
            {
                'AttributeKey': 'EventName',
                'AttributeValue': 'GenerateDataKey'
            },
            {
                'AttributeKey': 'EventName',
                'AttributeValue': 'Sign'
            },
            {
                'AttributeKey': 'EventName',
                'AttributeValue': 'Verify'
            },
        ],
        StartTime=start_time,
        EndTime=end_time,
    )

    for page in response_iterator:
        for event in page['Events']:
            events_summary.append({
                "EventId": event.get("EventId"),
                "EventName": event.get("EventName"),
                "Username": event.get("Username"),
                "EventTime": event.get("EventTime").isoformat(),
                "Resources": [
                    {"ResourceType": r["ResourceType"], "ResourceName": r["ResourceName"]}
                    for r in event.get("Resources", [])
                ]
            })
    return {"key_usage_events": events_summary}
