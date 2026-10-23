from datetime import datetime, timedelta
import os
from google.cloud import monitoring_v3
from observability_client import get_client_config
from observability_models import MetricQueryRequest, MetricDataPoint


def query_metric_window(metric_name: str, hours: int = 1) -> list[MetricDataPoint]:
    """Query recent datapoints for a named metric over a time window using Google Cloud Monitoring."""
    client_config = get_client_config()
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{client_config['project_id']}"

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)

    query_request = {
        "name": project_name,
        "filter": f'metric.type="{metric_name}"',
        "interval": {
            "start_time": {"seconds": int(start_time.timestamp())},
            "end_time": {"seconds": int(end_time.timestamp())},
        },
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    }

    results = []
    for series in client.list_time_series(request=query_request):
        for point in series.points:
            results.append(
                MetricDataPoint(
                    timestamp=point.interval.end_time.timestamp(),
                    value=float(point.value.double_value),
                    resource_labels=dict(series.resource.labels),
                    metric_labels=dict(series.metric.labels),
                )
            )
    return results