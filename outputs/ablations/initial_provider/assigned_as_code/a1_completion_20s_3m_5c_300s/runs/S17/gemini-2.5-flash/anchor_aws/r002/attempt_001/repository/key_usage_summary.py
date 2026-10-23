import boto3
from typing import List, Dict, Any
from security_models import KeyUsageEvent


def summarize_key_usage(key_id: str, region_name: str, lookback_hours: int = 24) -> List[KeyUsageEvent]:
    client = boto3.client("cloudtrail", region_name=region_name)
    events = []

    # CloudTrail LookupEvents can be used to find events for a specific resource (KeyId)
    # However, it has limitations on data retrieval and filtering. For a comprehensive summary,
    # integrating with CloudWatch Logs and CloudTrail Lake would be more robust.
    # For this exercise, we will use lookup_events with basic filtering.

    paginator = client.get_paginator("lookup_events")
    # Filtering by ResourceType 'AWS::KMS::Key' and ResourceName (key_id) can be done post-retrieval
    # or if the API supported direct filtering, but lookup_events is quite basic.
    # We'll fetch all KMS events and then filter by KeyId for demonstration.
    # In a real scenario, you'd query CloudWatch Logs for better filtering and performance.

    response_iterator = paginator.paginate(
        LookupAttributes=[
            {
                'AttributeKey': 'EventSource',
                'AttributeValue': 'kms.amazonaws.com'
            },
        ],
        MaxResults=50 # Limit for demonstration
    )

    for page in response_iterator:
        for event in page.get("Events", []):
            # Basic filtering for the specific key_id and relevant KMS actions
            # This is a simplified approach; in production, detailed parsing of CloudTrail events
            # from S3 or CloudWatch Logs would be necessary.
            cloud_trail_event = event.get("CloudTrailEvent")
            if cloud_trail_event:
                import json
                event_data = json.loads(cloud_trail_event)
                # Check if the event involves the specified key_id
                # This is a heuristic and might need refinement based on exact event structure
                resource_arn = event_data.get("resources")
                if resource_arn and any(key_id in str(r.get("resourceName")) for r in resource_arn if r.get("resourceType") == "AWS::KMS::Key"):
                    events.append(
                        KeyUsageEvent(
                            event_id=event_data.get("eventID"),
                            key_id=key_id, # Assume the requested key_id if filtered successfully
                            event_type=event_data.get("eventName"),
                            timestamp=event_data.get("eventTime"),
                            details=event_data
                        )
                    )
    return events
