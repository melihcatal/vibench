from google.cloud import monitoring_v3
from google.api import metric_service_v3
from observability_client import get_observability_client
from observability_models import MetricQueryRequest, MetricDataPoint


def query_metric_window(metric_name: str, hours: int = 1) -> list[MetricDataPoint]:
    client = get_observability_client()
    project_name = f"projects/{client.project_id}"
    
    query = (
        f"fetch gcp_metric"
        f" | metric type='{metric_name}'"
        f" | align rate({hours}h)"
        f" | every {hours}h"
    )
    
    result = client.query_time_series(name=project_name, query=query)
    
    points = []
    for series in result.time_series:
        for point in series.points:
            points.append(
                MetricDataPoint(
                    timestamp=point.interval.end_time.ToDatetime(),
                    value=float(point.value.double_value),
                    resource_labels=dict(series.resource.labels)
                )
            )
    
    return points