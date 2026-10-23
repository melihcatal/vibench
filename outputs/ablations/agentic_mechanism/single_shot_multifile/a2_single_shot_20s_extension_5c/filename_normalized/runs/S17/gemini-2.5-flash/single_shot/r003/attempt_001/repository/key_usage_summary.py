import os
from datetime import datetime
from security_client import get_cloudtrail_client
from security_models import KeyUsageSummaryRequest, KeyUsageSummaryResponse

def get_key_usage_summary(request: KeyUsageSummaryRequest) -> KeyUsageSummaryResponse:
    cloudtrail_client = get_cloudtrail_client()
    
    total_events = 0
    event_counts_by_type = {}
    
    paginator = cloudtrail_client.get_paginator('lookup_events')
    
    lookup_attributes = [
        {'AttributeKey': 'EventSource', 'AttributeValue': 'kms.amazonaws.com'}
    ]
    
    pages = paginator.paginate(
        LookupAttributes=lookup_attributes,
        StartTime=request.start_time,
        EndTime=request.end_time
    )

    for page in pages:
        for event in page['Events']:
            is_relevant_event = False
            if 'Resources' in event:
                for resource in event['Resources']:
                    if resource.get('ResourceName') == request.key_id:
                        is_relevant_event = True
                        break
            
            if is_relevant_event:
                total_events += 1
                event_name = event.get('EventName', 'UNKNOWN')
                event_counts_by_type[event_name] = event_counts_by_type.get(event_name, 0) + 1
    
    return KeyUsageSummaryResponse(
        total_events=total_events,
        event_counts_by_type=event_counts_by_type
    )
