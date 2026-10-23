import os
import datetime
from google.cloud import monitoring_v3
from google.cloud.monitoring_v3.types import aggregation
from .observability_models import TimeInterval, MetricQuery, MetricResponse, TimeSeriesPoint

project_name = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}"

_client = monitoring_v3.MetricServiceClient()

def query_time_series(query: MetricQuery, interval: TimeInterval) -> MetricResponse:
    req = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter=query.filter_str or f'metric.type = "{query.metric_type}"',
        interval=monitoring_v3.TimeInterval(
            start_time={"seconds": int(interval.start_time.timestamp())},
            end_time={"seconds": int(interval.end_time.timestamp())}
        ),
        view=monitoring_v3.ListTimeSeriesRequest.View.FULL,
    )
    if query.aggregation:
        req.aggregation = aggregation.Aggregation(**query.aggregation)
    points = []
    for series in _client.list_time_series(req):
        for point in series.points:
            ts = datetime.datetime.fromtimestamp(point.interval.end_time.seconds)
            val = point.value.double_value or point.value.int64_value or 0.0
            points.append(TimeSeriesPoint(timestamp=ts, value=float(val)))
    return MetricResponse(points=points)