# [SAME-SCENARIO] compare_metric_series.py

import os
from .observability_client import get_cloudwatch_client
from .observability_models import MetricQueryRequest, MetricResponse

SUPPORTED_SERVICES = {
    'cloudwatch': get_cloudwatch_client,
    # add other providers if needed
}

def compare_series(service, req1, req2):
    """Return side‑by‑side metric series for two queries (e.g., different resources or dimension sets).",
    if service not in SUPPORTED_SERVICES:
        raise ValueError(f"Unsupported service for comparison: {service}")
    client = SUPPORTED_SERVICES[service]()
    payload1 = req1.normalize()
    payload2 = req2.normalize()
    # Retrieve series for each request
    series1 = client.get_metric_statistics(
        Namespace=payload1.get('namespace', ""),
        MetricName=payload1['metric'],
        StartTime=payload1['start'] / 1000,
        EndTime=payload1['end'] / 1000,
        Period=int(payload1['granularity'] / 1000),
        Statistics=['Average'],
        Dimensions=[{'Name': k, 'Value': v} for k, v in payload1.get('dimensions', {}).items()]
    )['Datapoints']
    series2 = client.get_metric_statistics(
        Namespace=payload2.get('namespace', ""),
        MetricName=payload2['metric'],
        StartTime=payload2['start'] / 1000,
        EndTime=payload2['end'] / 1000,
        Period=int(payload2['granularity'] / 1000),
        Statistics=['Average'],
        Dimensions=[{'Name': k, 'Value': v} for k, v in payload2.get('dimensions', {}).items()]
    )['Datapoints']
    # Zip align timestamps (simple approach)
    combined = []
    for a, b in zip(series1, series2):
        combined.append({
            'timestamp': a['Timestamp'] if a.get('Timestamp') == b.get('Timestamp') else None,
            'value1': a['Average'],
            'value2': b['Average']
        })
    return MetricResponse(combined, metadata={'provider': service, 'comparison': 'side_by_side'})

# Example usage (for local testing)
if __name__ == '__main__':
    from datetime import datetime, timedelta, timezone
    req_a = MetricQueryRequest(
        metric_name='CPUUtilization',
        start_time=int((datetime.now(timezone.utc) - timedelta(minutes=20)).timestamp() * 1000),
        end_time=int(datetime.now(timezone.utc).timestamp() * 1000),
        granularity_ms=60 * 1000,
        dimensions={'InstanceId': 'i-instance1'}
    )
    req_b = MetricQueryRequest(
        metric_name='CPUUtilization',
        start_time=int((datetime.now(timezone.utc) - timedelta(minutes=20)).timestamp() * 1000),
        end_time=int(datetime.now(timezone.utc).timestamp() * 1000),
        granularity_ms=60 * 1000,
        dimensions={'InstanceId': 'i-instance2'}
    )
    print(compare_series('cloudwatch', req_a, req_b).datapoints)
