from typing import Dict, List, Tuple

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


def _series(request: MetricWindowRequest) -> List[MetricSeriesPoint]:
    config = load_config()
    client = monitoring_client()
    dimensions = normalize_dimensions(request.dimensions)
    filters = [f'metric.type = "{request.metric_type}"']
    filters.extend([f'resource.label."{k}" = "{v}"' for k, v in dimensions.items()])
    api_request = ListTimeSeriesRequest(
        name=metric_project_path(config.project_id),
        filter=" AND ".join(filters),
        interval=TimeInterval(start_time=request.start_time, end_time=request.end_time),
        view=ListTimeSeriesRequest.TimeSeriesView.FULL,
    )
    return [
        point_from_time_series_point(point)
        for series in client.list_time_series(request=api_request)
        for point in series.points
    ]


def compare_metric_series(
    left: MetricWindowRequest, right: MetricWindowRequest
) -> Tuple[List[MetricSeriesPoint], List[MetricSeriesPoint]]:
    return _series(left), _series(right)
