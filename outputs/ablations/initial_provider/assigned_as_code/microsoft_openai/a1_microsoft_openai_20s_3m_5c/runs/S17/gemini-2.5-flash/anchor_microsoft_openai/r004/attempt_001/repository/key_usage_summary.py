import boto3
from datetime import datetime, timedelta
from typing import Dict, Any, List

def summarize_key_usage(start_time_str: str, end_time_str: str) -> List[Dict[str, Any]]:
    cloudtrail_client = boto3.client('cloudtrail')

    # Convert string timestamps to datetime objects
    start_time = datetime.fromisoformat(start_time_str)
    end_time = datetime.fromisoformat(end_time_str)

    # Define common KMS and encryption-related event names
    # This list can be expanded based on specific audit requirements
    kms_event_names = [
        "Encrypt", "Decrypt", "GenerateDataKey", "GenerateDataKeyWithoutPlaintext",
        "ReEncrypt", "Sign", "Verify", "CreateKey", "ScheduleKeyDeletion",
        "CancelKeyDeletion", "EnableKeyRotation", "DisableKeyRotation",
        "PutKeyPolicy", "UpdateKeyDescription", "TagResource", "UntagResource"
    ]

    all_events = []
    next_token = None

    while True:
        if next_token:
            response = cloudtrail_client.lookup_events(
                LookupAttributes=[
                    {'AttributeKey': 'EventName', 'AttributeValue': event_name}
                    for event_name in kms_event_names
                ],
                StartTime=start_time,
                EndTime=end_time,
                NextToken=next_token
            )
        else:
            response = cloudtrail_client.lookup_events(
                LookupAttributes=[
                    {'AttributeKey': 'EventName', 'AttributeValue': event_name}
                    for event_name in kms_event_names
                ],
                StartTime=start_time,
                EndTime=end_time
            )

        events = response.get('Events', [])
        all_events.extend(events)

        next_token = response.get('NextToken')
        if not next_token:
            break

    summary = []
    for event in all_events:
        summary.append({
            'EventId': event.get('EventId'),
            'EventName': event.get('EventName'),
            'EventTime': event.get('EventTime').isoformat(),
            'Username': event.get('Username'),
            'Resources': [{'ResourceType': r.get('ResourceType'), 'ResourceName': r.get('ResourceName')} for r in event.get('Resources', []) if r.get('ResourceType') == 'AWS::KMS::Key'],
            'CloudTrailEvent': event.get('CloudTrailEvent') # Full event for deeper analysis if needed
        })

    return summary
