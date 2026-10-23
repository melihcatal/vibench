import json

from google.cloud import monitoring_v3

from observability_client import get_monitoring_client
from observability_models import MetricPoint

def _fetch_series(client, project_id, metric_type, start_time, end_time, filter_string, period_seconds):
    full_filter = f"metric.type = {json.dumps(metric_type)}"
    if filter_string:
        full_filter += f" AND {filter_string}"

    series = client.list_time_series(request={
        "name": f"projects/{project_id}",
        "filter": full_filter,
        "interval": {
            "start_time": {"seconds": int(start_time)}
            ,
            "end_time": {"seconds": int(end_time)}
        },
        "aggregation": {
            "alignment_period": {"seconds": period_seconds},
            "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN
        },
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
    })

    data_points = []
    for timeseries in series:
        for point in timeseries.points:
            kind = point.value._pb.WhichOneof("value")
            if kind not in ("double_value", "int64_value"):
                raise ValueError("Expected a scalar numeric metric")
            data_points.append(MetricPoint(timestamp=point.interval.end_time.timestamp(), value=float(getattr(point.value, kind))))
    return sorted(data_points, key=lambda p: p.timestamp)

def compare_metric_series(payload, config=None):
    config = config or {}
    client = get_monitoring_client()

    project_id = config["project_id"]
    metric_type = payload["metric"]
    start_time = payload["start_time"]
    end_time = payload["end_time"]
    period_seconds = config.get("period_seconds", 60)

    series1_data = _fetch_series(client, project_id, metric_type, start_time, end_time, payload["filter1"], period_seconds)
    series2_data = _fetch_series(client, project_id, metric_type, start_time, end_time, payload["filter2"], period_seconds)

    return {
        "series1": [p.__dict__ for p in series1_data],
        "series2": [p.__dict__ for p in series2_data],
    }
