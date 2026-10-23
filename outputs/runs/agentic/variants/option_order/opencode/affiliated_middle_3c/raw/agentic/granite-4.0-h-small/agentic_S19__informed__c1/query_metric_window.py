# [SAME-SCENARIO] query_metric_window.py

import os
from .observability_client import get_cloudwatch_client
from .observability_models import MetricQueryRequest, MetricResponse

SUPPORTED_SERVICES = {
    'cloudwatch': get_cloudwatch_client,
    # Add other same-scenario providers here if needed
}

def query_datapoints(service, req):
    """Return datapoints for the given provider and request.",
    try:
        client = SUPPORTED_SERVICES[service]()
    except KeyError:
        raise ValueError(f"Unsupported service for same-scenario query: {service}")
    # Convert request to provider-specific format (placeholder)
    provider_payload = req.normalize()
    # Example CloudWatch call (replace with appropriate SDK call for other services)
    if service == 'cloudwatch':
        response = client.get_metric_statistics(
            Namespace=provider_payload['namespace'],
            MetricName=provider_payload['metric'],
            StartTime=provider_payload['start'] / 1000,
            EndTime=provider_payload['end'] / 1000,
            Period=int(provider_payload['granularity'] / 1000),
            Statistics=['Average'],
            Dimensions=[{'Name': 'InstanceId', 'Value': d} for d in provider_payload['resources']]
        )
        datapoints = response.get('Datapoints', [])
    else:
        raise NotImplementedError(f"Query not implemented for {service}")
    return MetricResponse(datapoints)

# Example usage (for local testing)
if __name__ == '__main__':
    req = MetricQueryRequest(
        metric_name='CPUUtilization',
        start_time=int((datetime.utcnow() - timedelta(minutes=30)).timestamp() * 1000),
        end_time=int(datetime.utcnow().timestamp() * 1000),
        granularity_ms=60 * 1000,
        resources=['i-1234567890abcdef0']
    )
    print(query_datapoints('cloudwatch', req).datapoints)
