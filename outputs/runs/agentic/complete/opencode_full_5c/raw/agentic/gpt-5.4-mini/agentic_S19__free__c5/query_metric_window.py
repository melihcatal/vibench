from datetime import datetime
from typing import Dict, List

from google.cloud.monitoring_v3 import ListTimeSeriesRequest, TimeInterval

from observability_client import (
    load_config,
    metric_project_path,
    monitoring_client,
    normalize_dimensions,
)
from observability_models import (
    MetricWindowRequest,
    MetricSeriesPoint,
    point_from_time_series_point,
)


def query_metric_window(request: MetricWindowRequest) -> List[MetricSeriesPoint]:
    config = load_config()
    client = monitoring_client()
    interval = TimeInterval(start_time=request.start_time, end_time=request.end_time)
    filter_parts = [f'metric.type = "{request.metric_type}"']
    dimensions: Dict[str, str] = normalize_dimensions(request.dimensions)
    for key, value in dimensions.items():
        filter_parts.append(f'resource.label."{key}" = "{value}"')
    api_request = ListTimeSeriesRequest(
        name=metric_project_path(config.project_id),
        filter=" AND ".join(filter_parts),
        interval=interval,
        view=ListTimeSeriesRequest.TimeSeriesView.FULL,
    )
    series = client.list_time_series(request=api_request)
    points: List[MetricSeriesPoint] = []
    for item in series:
        for point in item.points:
            points.append(point_from_time_series_point(point))
    return points
