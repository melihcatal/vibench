from google.cloud import monitoring_v3
from google.api import label_pb2
from observability_client import get_client_config
from datetime import datetime, timedelta


def filter_metric_dimensions(metric_type: str, dimension_filters: dict, hours: int = 1, project_id: str = None):
    config = get_client_config()
    project_id = project_id or config.get("GOOGLE_CLOUD_PROJECT")
    
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
    
    filter_parts = [f"metric.type=\"{metric_type}\""]
    for key, value in dimension_filters.items():
        filter_parts.append(f"metric.labels.{key}=\"{value}\"")
    
    query = " AND ".join(filter_parts)
    
    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": query,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )
    
    return [
        {
            "metric": {
                "type": series.metric.type,
                "labels": dict(series.metric.labels),
            },
            "resource": {
                "type": series.resource.type,
                "labels": dict(series.resource.labels),
            },
            "points": [
                {
                    "interval": {
                        "start_time": point.interval.start_time.ToDatetime(),
                        "end_time": point.interval.end_time.ToDatetime(),
                    },
                    "value": point.value.double_value,
                }
                for point in series.points
            ],
        }
        for series in results
    ]