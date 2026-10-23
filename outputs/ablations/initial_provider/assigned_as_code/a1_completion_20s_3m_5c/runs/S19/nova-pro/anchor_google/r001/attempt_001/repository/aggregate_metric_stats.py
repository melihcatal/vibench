import json

from google.cloud import monitoring_v3

from observability_client import get_client
from observability_models import Aggregation, AlignmentPeriod


def aggregate_metric_stats(payload, config=None):
    config = config or {}
    client = get_client()
    series = client.list_time_series(request={"name": f"projects/{config['project_id']}",
        "filter": "metric.type = " + json.dumps(payload["metric"]),
        "interval": {"start_time": {"seconds": int(payload["start_time"])},
                       "end_time": {"seconds": int(payload["end_time"])}},
        "aggregation": {"alignment_period": AlignmentPeriod(seconds=config.get("period_seconds", 60)),
                          "per_series_aligner": Aggregation.Aligner.ALIGN_MEAN},
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL})
    stats = []
    for timeseries in series:
        for point in timeseries.points:
            kind = point.value._pb.WhichOneof("value")
            if kind not in ("double_value", "int64_value"):
                raise ValueError("Expected a scalar numeric metric")
            stats.append(float(getattr(point.value, kind)))
    return {"stats": {"count": len(stats), "sum": sum(stats), "mean": sum(stats) / len(stats) if stats else 0}})