import os
from observability_client import CloudWatchClient
from observability_models import MetricAggregateRequest


def metric_summary(metric_name: str, start_time: str, end_time: str, region: str = None):
    """Summarize recent metric trends or anomalies using Amazon CloudWatch Metrics.

    Uses aggregated statistics to provide a concise overview.
    """
    region = region or os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    client = CloudWatchClient(region=region)
    agg_req = MetricAggregateRequest(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        period=300,
        statistics=['Average', 'Sum', 'Maximum', 'Minimum']
    )
    stats = client.get_metric_statistics(agg_req)
    # Simple summary dictionary
    return {
        'average': stats.get('Average'),
        'sum': stats.get('Sum'),
        'max': stats.get('Maximum'),
        'min': stats.get('Minimum'),
        'missing_data': agg_req.get('dimensions', [])
    }
