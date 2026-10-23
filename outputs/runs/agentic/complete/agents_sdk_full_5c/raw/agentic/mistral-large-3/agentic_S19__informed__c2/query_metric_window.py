from google.cloud import monitoring_v3
from google.api import metric_service_v3
from google.api import label_pb2
from observability_client import get_observability_client
from observability_models import MetricQueryRequest, MetricDataPoint
from datetime import datetime, timedelta
from typing import List


def query_metric_window(metric_type: str, hours: int = 1, project_id: str = None) -> List[MetricDataPoint]:
    """Query recent datapoints for a named metric over a time window using Google Cloud Monitoring."""
    client = get_observability_client(monitoring_v3.MetricServiceClient)
    if not project_id:
        project_id = get_observability_client("GOOGLE_CLOUD_PROJECT")

    now = datetime.utcnow()
    start_time = now - timedelta(hours=hours)

    query_request = MetricQueryRequest(
        metric_type=metric_type,
        start_time=start_time,
        end_time=now
    )

    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": int(now.timestamp())},
            "start_time": {"seconds": int(start_time.timestamp())},
        }
    )

    results = []
    for result in client.list_time_series(
        name=f"projects/{project_id}",
        filter=f'metric.type="{metric_type}"',
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