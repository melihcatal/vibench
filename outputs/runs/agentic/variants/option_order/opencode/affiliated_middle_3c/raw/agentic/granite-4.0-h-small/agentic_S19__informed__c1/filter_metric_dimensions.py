# [SAME-SCENARIO] filter_metric_dimensions.py

import os
from .observability_client import get_cloudwatch_client
from .observability_models import MetricQueryRequest, MetricResponse

SUPPORTED_SERVICES = {
    'cloudwatch': get_cloudwatch_client,
    # add other same-scenario providers as needed
}

def filter_data(service, req):
    """Return metric data filtered by resource labels or dimensions.",
    try:
        client = SUPPORTED_SERVICES[service]()
    except KeyError:
        raise ValueError(f"Unsupported service for filtering: {service}")
    provider_payload = req.normalize()
    if service == 'cloudwatch':
        # CloudWatch dimensions are passed via the Dimensions param
        response = client.get_metric_statistics(
            Namespace=provider_payload.get('namespace', ""),
            MetricName=provider_payload['metric'],
            StartTime=provider_payload['start'] / 1000,
            EndTime=provider_payload['end'] / 1000,
            Period=int(provider_payload['granularity'] / 1000),
            Statistics=['Average'],
            Dimensions=[{'Name': k, 'Value': v} for k, v in provider_payload.get('dimensions', {}).items()]
        )
        datapoints = response.get('Datapoints', [])
    else:
        raise NotImplementedError(f"Filtering not implemented for {service}")
    return MetricResponse(datapoints)

# Example usage (for local testing)
if __name__ == '__main__':
    from datetime import datetime, timedelta, timezone
    req = MetricQueryRequest(
        metric_name='CPUUtilization',
        start_time=int((datetime.now(timezone.utc) - timedelta(minutes=10)).timestamp() * 1000),
        end_time=int(datetime.now(timezone.utc).timestamp() * 1000),
        granularity_ms=60 * 1000,
        resources=['i-1234567890abcdef0'],
        # dimensions example: {'InstanceId': 'i-1234567890abcdef0'}
        dimensions={'InstanceId': 'i-1234567890abcdef0'}
    )
    print(filter_data('cloudwatch', req).datapoints)
