import os
from observability_client import get_client
from observability_models import MetricQueryRequest, MetricQueryResponse

# ----------- SCORED IMPLEMENTATION ------------
# GCP Monitoring (managed metrics) via monitoring.googleapis.com
# Provider signal: imported client from google.api_core.monitored_resource

def query_metric_window(metric_type: str, window_seconds: int = 3600, **kwargs) -> MetricQueryResponse:
    """Query recent datapoints for a named metric over a time window using GCP Monitoring API.

    Args:
        metric_type: The metric type as defined in GCP Monitoring (e.g., 'gcp.pubsub.topic/numMessages').
        window_seconds: Lookback window in seconds. Defaults to 3600 (1 hour).
        kwargs: Additional filters (e.g., resource type, label filters) passed to the request.

    Returns:
        MetricQueryResponse containing the time series data.
    """
    client = get_client()  # creates google.cloud.monitoring_v3.MetricServiceClient
    end_time = client.now()
    start_time = end_time - client.Duration(seconds=window_seconds)
    request = MetricQueryRequest(
        name=f"projects/{os.getenv('GCP_PROJECT')}/metricDescriptors/{metric_type}",
        interval={'startTime': start_time, 'endTime': end_time},
        aggregation={'alignmentPeriod': f'{window_seconds}s', 'perSeriesAligner': 'ALIGN_MEAN'},
        **kwargs
    )
    response = client.query_time_series(request)
    # normalize response for downstream helpers
    return MetricQueryResponse.from_api(response)
