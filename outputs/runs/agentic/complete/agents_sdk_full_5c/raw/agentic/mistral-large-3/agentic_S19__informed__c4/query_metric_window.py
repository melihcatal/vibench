from google.cloud import monitoring_v3
from google.api import metric_service_v3
from google.api import label_pb2
from observability_client import get_client_config
from datetime import datetime, timedelta


def query_metric_window(metric_type: str, hours: int = 1, project_id: str = None):
    """Query recent datapoints for a named metric over a time window using Google Cloud Monitoring."""
    client_config = get_client_config()
    project_id = project_id or client_config.get("GOOGLE_CLOUD_PROJECT")
    
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"
    
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)
    
    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": int(end_time.timestamp())},
            "start_time": {"seconds": int(start_time.timestamp())},
        }
    )
    
    query = f"metric.type=\"{metric_type}\""
    results = client.list_time_series(
        name=project_name,
        filter_=query,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
    )
    
    return [
        {
            "timestamp": point.interval.end_time.ToDatetime(),
            "value": point.value.double_value,
            "resource": series.resource.type,
            "labels": dict(series.resource.labels)
        }
        for series in results
        for point in series.points
    ]