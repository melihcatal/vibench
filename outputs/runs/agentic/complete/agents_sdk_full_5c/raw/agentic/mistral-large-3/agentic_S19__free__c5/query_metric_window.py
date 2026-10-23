from google.cloud import monitoring_v3
from google.api import metric_service_v3
from observability_client import get_monitoring_client
from observability_models import MetricQueryRequest, MetricDataPoint
from datetime import datetime, timedelta

def query_metric_window(metric_type: str, project_id: str, hours: int = 1) -> list[MetricDataPoint]:
    client = get_monitoring_client()
    project_name = f"projects/{project_id}"
    
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)
    
    query_request = {
        "name": project_name,
        "filter": f'metric.type="{metric_type}"',
        "interval": {
            "start_time": {"seconds": int(start_time.timestamp())},
            "end_time": {"seconds": int(end_time.timestamp())}
        },
        "view": metric_service_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
    }
    
    results = []
    for series in client.list_time_series(request=query_request):
        for point in series.points:
            results.append(
                MetricDataPoint(
                    timestamp=point.interval.end_time.ToDatetime(),
                    value=float(point.value.double_value),
                    resource_labels=dict(series.resource.labels)
                )
            )
    
    return results