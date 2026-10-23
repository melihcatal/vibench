from google.cloud import monitoring_v3
from observability_client import monitoring_client, project_name, metric_type
from observability_models import parse_window


def metric_summary(metric, minutes=60):
    client = monitoring_client()
    project = project_name()
    start, end = parse_window(minutes)
    interval = monitoring_v3.TimeInterval()
    interval.end_time.FromDatetime(end)
    interval.start_time.FromDatetime(start)
    res = client.list_time_series(request={"name": project, "filter": f'metric.type = "{metric_type(metric)}"', "interval": interval, "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL})
    values = []
    for s in res:
        for p in s.points:
            values.append(p.value.double_value or p.value.int64_value)
    if not values:
        return {"trend": "flat", "anomalies": []}
    trend = "up" if values[-1] > values[0] else "down" if values[-1] < values[0] else "flat"
    return {"trend": trend, "anomalies": [v for v in values if v > (sum(values) / len(values)) * 2]}
