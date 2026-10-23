from typing import List

from google.cloud.monitoring_v3 import ListTimeSeriesRequest, TimeInterval

from observability_client import load_config, metric_project_path, monitoring_client
from observability_models import (
    MetricWindowRequest,
    MetricAggregateStats,
    stats_from_values,
)


def aggregate_metric_stats(request: MetricWindowRequest) -> MetricAggregateStats:
    config = load_config()
    client = monitoring_client()
    api_request = ListTimeSeriesRequest(
        name=metric_project_path(config.project_id),
        filter=f'metric.type = "{request.metric_type}"',
        interval=TimeInterval(start_time=request.start_time, end_time=request.end_time),
        view=ListTimeSeriesRequest.TimeSeriesView.FULL,
    )
    values: List[float] = []
    for series in client.list_time_series(request=api_request):
        for point in series.points:
            if point.value.double_value:
                values.append(float(point.value.double_value))
            elif point.value.int64_value:
                values.append(float(point.value.int64_value))
    return stats_from_values(values)
