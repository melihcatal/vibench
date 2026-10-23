from google.cloud import monitoring_v3
from google.api import metric_service_v3
from observability_client import get_observability_client
from observability_models import MetricDataPoint, MetricQueryRequest
from datetime import datetime, timedelta
from typing import List, Dict


def filter_metric_dimensions(
    metric_type: str, 
    dimension_filters: Dict[str, str], 
    hours: int = 1, 
    project_id: str = None
) -> List[MetricDataPoint]:
    """Query metric data filtered by resource labels or dimensions using Google Cloud Monitoring."""
    client = get_observability_client(monitoring_v3.MetricServiceClient)
    if not project_id:
        project_id = get_observability_client("GOOGLE_CLOUD_PROJECT")

    now = datetime.utcnow()
    start_time = now - timedelta(hours=hours)

    filter_parts = [f'metric.type="{metric_type}"']
    for key, value in dimension_filters.items():
        filter_parts.append(f'resource.label.{key}="{value}"')

    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": int(now.timestamp())},
            "start_time": {"seconds": int(start_time.timestamp())},
        }
    )

    results = []
    for result in client.list_time_series(
        name=f"projects/{project_id}",
        filter=" AND ".join(filter_parts),
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
    ):
        for point in result.points:
            results.append(MetricDataPoint(
                timestamp=point.interval.end_time.ToDatetime(),
                value=float(point.value.double_value),
                resource_labels=dict(result.resource.labels)
            ))

    return results