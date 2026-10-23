import json

from google.cloud import monitoring_v3

from observability_client import get_metric_client
from observability_models import MetricAggregationPayload, MetricQueryResponse, TimeSeriesPoint


def aggregate_metric_stats(payload: MetricAggregationPayload, config=None):
    config = config or {}
    client = get_metric_client()

    # Map aggregator string to monitoring_v3.Aggregation.Aligner enum
    aggregator_map = {
        "mean": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        "min": monitoring_v3.Aggregation.Aligner.ALIGN_MIN,
        "max": monitoring_v3.Aggregation.Aligner.ALIGN_MAX,
        "sum": monitoring_v3.Aggregation.Aligner.ALIGN_SUM,
        "count": monitoring_v3.Aggregation.Aligner.ALIGN_COUNT,
    }
    aligner = aggregator_map.get(payload.aggregator.lower(), monitoring_v3.Aggregation.Aligner.ALIGN_MEAN)

    series = client.list_time_series(request={
        "name": f"projects/{config['project_id']}",
        "filter": "metric.type = " + json.dumps(payload.metric),
        "interval": {
            "start_time": {"seconds": int(payload.start_time)},
            "end_time": {"seconds": int(payload.end_time)}
        },
        "aggregation": {
            "alignment_period": {"seconds": payload.period_seconds},
            "per_series_aligner": aligner
        },
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
