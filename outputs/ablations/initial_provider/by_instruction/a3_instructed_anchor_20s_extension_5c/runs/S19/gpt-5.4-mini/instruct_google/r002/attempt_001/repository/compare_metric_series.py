from google.cloud import monitoring_v3
from observability_client import monitoring_client, project_name, metric_type
from observability_models import parse_window


def compare_metric_series(metric, left_dimensions=None, right_dimensions=None, minutes=60):
    client = monitoring_client()
    project = project_name()
    start, end = parse_window(minutes)
    interval = monitoring_v3.TimeInterval()
    interval.end_time.FromDatetime(end)
    interval.start_time.FromDatetime(start)

    def fetch(dims):
        flt = [f'metric.type = "{metric_type(metric)}"']
        for k, v in (dims or {}).items():
            flt.append(f'metric.labels."{k}" = "{v}"')
        res = client.list_time_series(request={"name": project, "filter": " AND ".join(flt), "interval": interval, "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL})
        vals = []
        for s in res:
            for p in s.points:
                vals.append(p.value.double_value or p.value.int64_value)
        return vals

    left = fetch(left_dimensions)
    right = fetch(right_dimensions)
    return {"left_count": len(left), "right_count": len(right), "left_avg": (sum(left) / len(left)) if left else None, "right_avg": (sum(right) / len(right)) if right else None}
