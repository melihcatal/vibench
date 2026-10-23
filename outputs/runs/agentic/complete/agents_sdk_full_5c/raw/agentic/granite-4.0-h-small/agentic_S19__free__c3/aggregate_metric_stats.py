import os
from observability_client import get_client
from observability_models import MetricAggregateRequest, MetricAggregateResponse

# ----------- SCORED IMPLEMENTATION ------------
# GCP Monitoring (managed metrics) via monitoring.googleapis.com
# Provider signal: imported client from google.api_core.monitored_resource

def aggregate_metric_stats(metric_type: str, window_seconds: int = 3600, **kwargs) -> MetricAggregateResponse:
    """Retrieve aggregated statistics for a metric over a time window using GCP Monitoring API.

    Args:
        metric_type: Metric descriptor name (e.g., 'gcp.pubsub.topic/numMessages').
        window_seconds: Lookback window in seconds. Defaults to 3600.
        kwargs: Additional aggregation filters or parameters (e.g., alignmentPeriod, perSeriesAligner).

    Returns:
        MetricAggregateResponse with aggregated values (mean, sum, count, etc.).
    """
    client = get_client()
    end_time = client.now()
    start_time = end_time - client.Duration(seconds=window_seconds)
    request = MetricAggregateRequest(
        name=f"projects/{os.getenv('GCP_PROJECT')}/metricDescriptors/{metric_type}",
        interval={'startTime': start_time, 'endTime': end_time},
        aggregation={'alignmentPeriod': f'{window_seconds}s', **kwargs}
    )
    response = client.aggregate_metric_data(request)
    return MetricAggregateResponse.from_api(response)
