"""
key_usage_summary.py - Summarize key usage and crypto events using AWS CloudTrail.
"""
from security_client import get_cloudtrail_client
from datetime import datetime, timedelta

def summarize_kms_key_usage(key_arn: str, look_back_days: int = 7) -> list:
    """
    Summarizes usage events for a specific AWS KMS key from CloudTrail logs.

    Args:
        key_arn: The ARN of the KMS key to summarize usage for.
        look_back_days: The number of days to look back for events.

    Returns:
        A list of dictionaries, where each dictionary represents a relevant CloudTrail event.
    """
    cloudtrail_client = get_cloudtrail_client()
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=look_back_days)

    events = []
    try:
        paginator = cloudtrail_client.get_paginator('lookup_events')
        response_iterator = paginator.paginate(
            LookupAttributes=[
                {'AttributeKey': 'ResourceName', 'AttributeValue': key_arn}
            ],
            StartTime=start_time,
            EndTime=end_time,
            # Only interested in KMS events
            Filters=[
                {'AttributeKey': 'EventSource', 'AttributeValue': 'kms.amazonaws.com'}
            ]
        )

        for page in response_iterator:
            events.extend(page.get('Events', []))

    except Exception as e:
        print(f"Error summarizing KMS key usage from CloudTrail: {e}")
        raise

    return events
