import json

from google.cloud import monitoring_v3

from observability_client import get_metric_client
from observability_models import MetricComparisonPayload, MetricCompareResponse, TimeSeriesPoint


def _get_series_data(client, project_id, metric, start_time, end_time, filters, period_seconds=60):
    filter_parts = [f"metric.type = {json.dumps(metric)}"]
    for dim, val in filters.items():
        filter_parts.append(f"metric.labels.{dim} = {json.dumps(val)}")
    full_filter = " AND ".join(filter_parts)

    series = client.list_time_series(request={
        "name": f"projects/{project_id}",
        "filter": full_filter,
        "interval": {
            "start_time": {"seconds": int(start_time)},
            "end_time": {"seconds": int(end_time)}
        },
        "aggregation": {"alignment_period": {"seconds": period_seconds},
                        "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN},
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
    })

    points = []
    for timeseries in series:
        for point in timeseries.points:
            kind = point.value._pb.WhichOneof("value")
            if kind not in ("double_value", "int64_value"):
                raise ValueError("Expected a scalar numeric metric")
            points.append(TimeSeriesPoint(timestamp=point.interval.end_time.timestamp(), value=float(getattr(point.value, kind))))
    return sorted(points, key=lambda p: p.timestamp)


def compare_metric_series(payload: MetricComparisonPayload, config=None):
    config = config or {}
    client = get_metric_client()

    series_a_points = _get_series_data(client, config['project_id'], payload.metric,
                                       payload.start_time, payload.end_time, payload.filter_a,
                                       config.get("period_seconds", 60))
    series_b_points = _get_series_data(client, config['project_id'], payload.metric,
                                       payload.start_time, payload.end_time, payload.filter_b,
                                       config.get("period_seconds", 60))

    return MetricCompareResponse(series_a=series_a_points, series_b=series_b_points)
