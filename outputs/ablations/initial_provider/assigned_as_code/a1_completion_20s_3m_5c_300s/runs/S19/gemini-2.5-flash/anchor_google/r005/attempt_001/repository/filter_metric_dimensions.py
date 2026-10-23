import json

from google.cloud import monitoring_v3

from observability_client import get_metric_client
from observability_models import MetricFilterPayload, MetricQueryResponse, TimeSeriesPoint


def filter_metric_dimensions(payload: MetricFilterPayload, config=None):
    config = config or {}
    client = get_metric_client()

    filter_parts = [f"metric.type = {json.dumps(payload.metric)}"]
    for dim, val in payload.filters.items():
        filter_parts.append(f"metric.labels.{dim} = {json.dumps(val)}")

    full_filter = " AND ".join(filter_parts)

    series = client.list_time_series(request={
        "name": f"projects/{config['project_id']}",
        "filter": full_filter,
        "interval": {
            "start_time": {"seconds": int(payload.start_time)},
            "end_time": {"seconds": int(payload.end_time)}
        },
        "aggregation": {"alignment_period": {"seconds": config.get("period_seconds", 60)},
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

    return MetricQueryResponse(points=sorted(points, key=lambda p: p.timestamp))
