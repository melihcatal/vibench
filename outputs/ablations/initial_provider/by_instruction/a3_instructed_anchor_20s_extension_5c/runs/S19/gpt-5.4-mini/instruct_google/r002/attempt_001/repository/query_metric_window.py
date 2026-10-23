from google.cloud import monitoring_v3
from observability_client import monitoring_client, project_name, metric_type
from observability_models import parse_window, normalize_dimensions, normalize_points


def query_metric_window(metric, minutes=60, dimensions=None):
    client = monitoring_client()
    project = project_name()
    start, end = parse_window(minutes)
    interval = monitoring_v3.TimeInterval()
    interval.end_time.FromDatetime(end)
    interval.start_time.FromDatetime(start)
    flt = [f'metric.type = "{metric_type(metric)}"']
    for k, v in normalize_dimensions(dimensions).items():
        flt.append(f'metric.labels."{k}" = "{v}"')
    results = client.list_time_series(
        request={
            "name": project,
            "filter": " AND ".join(flt),
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )
    points = []
    for series in results:
        for p in series.points:
            points.append({"time": p.interval.end_time, "value": p.value.double_value or p.value.int64_value})
    return normalize_points(points)
