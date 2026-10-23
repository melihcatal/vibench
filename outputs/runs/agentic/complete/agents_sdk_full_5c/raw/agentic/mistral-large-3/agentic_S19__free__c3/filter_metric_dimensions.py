from datetime import datetime, timedelta
import os
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client
from observability_models import DimensionFilterRequest, MetricDataPoint


def filter_metric_dimensions(request: DimensionFilterRequest) -> list[MetricDataPoint]:
    client = get_monitoring_client()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=request.window_hours)
    
    filter_parts = [f'metric.type="{request.metric_type}"']
    for key, value in request.dimensions.items():
        filter_parts.append(f'resource.label.{key}="{value}"')
    
    series_request = {
        "name": f"projects/{project_id}",
        "filter": " AND ".join(filter_parts),
        "interval": {
            "start_time": {"seconds": int(start_time.timestamp())},
            "end_time": {"seconds": int(end_time.timestamp())},
        },
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
    }
    
    time_series = client.list_time_series(request=series_request)
    
    results = []
    for series in time_series:
        for point in series.points:
            results.append(
                MetricDataPoint(
                    timestamp=point.interval.end_time.timestamp(),
                    value=float(point.value.double_value),
                    resource_labels=dict(series.resource.labels),
                    metric_labels=dict(series.metric.labels)
                )
            )
    
    return results