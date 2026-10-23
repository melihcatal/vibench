import boto3

def summarize_key_usage(key_id: str, start_time: int, end_time: int) -> list:
    cloudtrail_client = boto3.client('cloudtrail')
    events = []
    paginator = cloudtrail_client.get_paginator('lookup_events')

    # Filtering by resource name (key ARN) is not directly supported in lookup_events
    # We will fetch events and then filter them client-side based on the key_id in the event.
    # This is a simplified approach, for a real-world scenario, consider CloudWatch Logs integration.
    for page in paginator.paginate(
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
            }
        ],
        StartTime=start_time,
        EndTime=end_time
    ):
        for event in page['Events']:
            # A very basic client-side filter. More robust parsing of CloudTrail event data might be needed.
            if key_id in str(event):
                events.append({
                    "EventId": event['EventId'],
                    "EventName": event['EventName'],
                    "EventTime": event['EventTime'],
                    "Username": event['Username']
                })
    return events
