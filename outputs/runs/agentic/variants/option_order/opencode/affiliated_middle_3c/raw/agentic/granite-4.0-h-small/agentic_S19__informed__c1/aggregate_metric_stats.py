# [SAME-SCENARIO] aggregate_metric_stats.py

import os
from .observability_client import get_cloudwatch_client
from .observability_models import MetricQueryRequest, MetricResponse

SUPPORTED_SERVICES = {
    'cloudwatch': get_cloudwatch_client,
    # add other providers as needed
}

def aggregate_stats(service, req):
    """Return aggregated statistics for the given service and request.",
    try:
        client = SUPPORTED_SERVICES[service]()
    except KeyError:
        raise ValueError(f"Unsupported service for aggregation: {service}")
    provider_payload = req.normalize()
    if service == 'cloudwatch':
        response = client.get_metric_statistics(
            Namespace=provider_payload['namespace'] if 'namespace' in provider_payload else "",
            MetricName=provider_payload['metric'],
            StartTime=provider_payload['start'] / 1000,
            EndTime=provider_payload['end'] / 1000,
            Period=int(provider_payload['granularity'] / 1000),
            Statistics=['Average', 'Sum', 'Minimum', 'Maximum'],
            Dimensions=[{'Name': 'InstanceId', 'Value': d} for d in provider_payload['resources']]
        )
        datapoints = response.get('Datapoints', [])
        # Build a simple stats dict (placeholder)
        stats = {
            'Average': [dp['Average'] for dp in datapoints],
            'Sum': [dp['Sum'] for dp in datapoints],
            'Minimum': [dp['Minimum'] for dp in datapoints],
            'Maximum': [dp['Maximum'] for dp in datapoints]
        }
    else:
        raise NotImplementedError(f"Aggregation not implemented for {service}")
    return MetricResponse(stats, metadata={'service': service})

# Example usage (for local testing)
if __name__ == '__main__':
    from datetime import datetime, timedelta, timezone
    req = MetricQueryRequest(
        metric_name='CPUUtilization',
        start_time=int((datetime.now(timezone.utc) - timedelta(minutes=15)).timestamp() * 1000),
        end_time=int(datetime.now(timezone.utc).timestamp() * 1000),
        granularity_ms=60 * 1000,
        resources=['i-1234567890abcdef0']
    )
    print(aggregate_stats('cloudwatch', req).datapoints)
