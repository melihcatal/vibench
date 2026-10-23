import os
from typing import List, Dict, Any
import boto3
from security_models import KeyUsageEvent

class CloudTrailClientWrapper:
    def __init__(self):
        self.cloudtrail_client = boto3.client(
            'cloudtrail',
            region_name=os.environ.get('AWS_REGION', 'us-east-1')
        )

def summarize_key_usage(lookup_attributes: List[Dict[str, str]]) -> List[KeyUsageEvent]:
    cloudtrail_client = CloudTrailClientWrapper().cloudtrail_client
    response = cloudtrail_client.lookup_events(
        LookupAttributes=lookup_attributes,
        MaxResults=50 # Limiting for example purposes
    )

    events = []
    for event in response.get('Events', []):
        cloud_trail_event = event.get('CloudTrailEvent')
        # In a real scenario, you would parse the full CloudTrailEvent string (JSON)
        # to extract more detailed information. For this example, we'll extract basic fields.
        # This is a simplified parsing for demonstration.

        # Example of parsing, assuming CloudTrailEvent is a JSON string
        # For a full implementation, you'd parse the JSON string and extract more data.
        # For now, we will extract what's directly available or make reasonable assumptions.

        # Placeholder for actual parsing of CloudTrailEvent JSON string
        # if 'eventName' in parsed_event and 'resources' in parsed_event:
        #   key_id = next((r['resourceName'] for r in parsed_event['resources'] if r['resourceType'] == 'AWS::KMS::Key'), 'N/A')

        # Simplified extraction from the top-level event object for demonstration
        event_id = event.get('EventId', 'N/A')
        event_name = event.get('EventName', 'N/A')
        event_time = str(event.get('EventTime', 'N/A'))
        username = event.get('Username', 'N/A')
        resource_name = event.get('Resources')[0].get('ResourceName') if event.get('Resources') else 'N/A'

        events.append(KeyUsageEvent(
            event_id=event_id,
            event_name=event_name,
            event_time=event_time,
            key_id=resource_name, # Simplified: assuming resourceName is the key_id for KMS events
            source_ip_address=event.get('SourceIPAddress', 'N/A'),
            user_identity={'userName': username}
        ))

    return events
