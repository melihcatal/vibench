from datetime import datetime, timedelta
from security_models import KeyUsageSummaryConfig
from security_client import get_cloudtrail_client

def summarize_key_usage(config: KeyUsageSummaryConfig, lookup_attributes: list = None):
    client = get_cloudtrail_client(config.aws_region)

    if lookup_attributes is None:
        lookup_attributes = []
    
    # Example: Look for KMS events in the last 24 hours
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=24)

    events = []
    paginator = client.get_paginator('lookup_events')
    response_iterator = paginator.paginate(
        LookupAttributes=lookup_attributes, 
        StartTime=start_time,
        EndTime=end_time
    )

    for page in response_iterator:
        for event in page['Events']:
            if 'KMS' in event.get('EventSource', ''):
                events.append(event)
    
    summary = {
        "total_kms_events": len(events),
        "events": events
    }
    return summary
