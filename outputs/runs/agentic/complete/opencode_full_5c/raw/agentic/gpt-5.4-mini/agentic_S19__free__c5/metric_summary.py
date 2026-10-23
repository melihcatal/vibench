from datetime import datetime, timedelta
from typing import Dict, List

from google.cloud.monitoring_v3 import ListTimeSeriesRequest, TimeInterval

from observability_client import load_config, metric_project_path, monitoring_client
from observability_models import MetricAggregateStats, stats_from_values


def metric_summary(metric_type: str, hours: int = 24) -> Dict[str, float]:
    config = load_config()
    client = monitoring_client()
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)
    api_request = ListTimeSeriesRequest(
        name=metric_project_path(config.project_id),
        filter=f'metric.type = "{metric_type}"',
        interval=TimeInterval(start_time=start_time, end_time=end_time),
        view=ListTimeSeriesRequest.TimeSeriesView.FULL,
    )
    values: List[float] = []
    for series in client.list_time_series(request=api_request):
        for point in series.points:
            if point.value.double_value:
                values.append(float(point.value.double_value))
            elif point.value.int64_value:
                values.append(float(point.value.int64_value))
    stats: MetricAggregateStats = stats_from_values(values)
    return {
        "count": float(stats.count),
        "minimum": stats.minimum,
        "maximum": stats.maximum,
        "mean": stats.mean,
        "sum": stats.sum,
    }
