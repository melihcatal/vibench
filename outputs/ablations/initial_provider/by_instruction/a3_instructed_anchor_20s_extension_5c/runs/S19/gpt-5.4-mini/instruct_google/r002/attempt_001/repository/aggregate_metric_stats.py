from google.cloud import monitoring_v3
from observability_client import monitoring_client, project_name, metric_type
from observability_models import parse_window, normalize_dimensions


def aggregate_metric_stats(metric, minutes=60, dimensions=None):
    client = monitoring_client()
    project = project_name()
    start, end = parse_window(minutes)
    interval = monitoring_v3.TimeInterval()
    interval.end_time.FromDatetime(end)
    interval.start_time.FromDatetime(start)
    flt = [f'metric.type = "{metric_type(metric)}"']
    for k, v in normalize_dimensions(dimensions).items():
        flt.append(f'metric.labels."{k}" = "{v}"')
    series = client.list_time_series(
        request={
            "name": project,
            "filter": " AND ".join(flt),
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": {
                "alignment_period": {"seconds": 60},
                "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
            },
        }
    )
    values = []
    for s in series:
        for p in s.points:
            values.append(p.value.double_value or p.value.int64_value)
    return {"count": len(values), "min": min(values) if values else None, "max": max(values) if values else None, "avg": (sum(values) / len(values)) if values else None}
