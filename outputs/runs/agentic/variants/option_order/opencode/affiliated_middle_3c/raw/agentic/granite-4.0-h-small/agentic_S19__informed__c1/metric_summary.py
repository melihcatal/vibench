# [LATER-STEP] metric_summary.py

import os
from .observability_client import get_cloudwatch_client
from .observability_models import MetricQueryRequest, MetricResponse

SUPPORTED_SERVICES = {
    'cloudwatch': get_cloudwatch_client,
    # add other providers as needed
}

def summarize(service, req):
    """Return a concise summary (trend, anomaly flag) for the queried metric.",
    try:
        client = SUPPORTED_SERVICES[service]()
    except KeyError:
        raise ValueError(f"Unsupported service for summary: {service}")
    payload = req.normalize()
    if service == 'cloudwatch':
        # Simple example: compare average to static threshold
        stats = client.get_metric_statistics(
            Namespace=payload.get('namespace', ""),
            MetricName=payload['metric'],
            StartTime=payload['start'] / 1000,
            EndTime=payload['end'] / 1000,
            Period=int(payload['granularity'] / 1000),
            Statistics=['Average'],
            Dimensions=[{'Name': k, 'Value': v} for k, v in payload.get('dimensions', {}).items()]
        )
        datapoints = stats.get('Datapoints', [])
        if not datapoints:
            return {"message": "No data", "anomaly": False}
        averages = [dp['Average'] for dp in datapoints]
        avg_val = sum(averages) / len(averages)
        # Anomaly if > 80% above a baseline of 50 (placeholder logic)
        baseline = 50.0
        anomaly = avg_val > baseline * 1.8
        return {
            "trend": "average", 
            "average": avg_val,
            "anomaly": anomaly,
            "metric": payload['metric']
        }
    else:
        raise NotImplementedError(f"Summary not implemented for {service}")

# Example usage (for local testing)
if __name__ == '__main__':
    from datetime import datetime, timedelta, timezone
    req = MetricQueryRequest(
        metric_name='CPUUtilization',
        start_time=int((datetime.now(timezone.utc) - timedelta(minutes=30)).timestamp() * 1000),
        end_time=int(datetime.now(timezone.utc).timestamp() * 1000),
        granularity_ms=60 * 1000,
        dimensions={'InstanceId': 'i-1234567890abcdef0'}
    )
    print(summarize('cloudwatch', req))
