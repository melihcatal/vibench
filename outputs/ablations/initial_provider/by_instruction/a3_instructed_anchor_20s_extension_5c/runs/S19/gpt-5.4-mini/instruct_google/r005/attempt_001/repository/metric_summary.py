from datetime import datetime, timedelta, timezone

from google.cloud import monitoring_v3

from observability_client import client, project_name


def metric_summary(metric_type: str, minutes: int = 1440, project_id: str | None = None):
    c = client()
    project = project_name(project_id)
    interval = monitoring_v3.TimeInterval(end_time=datetime.now(timezone.utc), start_time=datetime.now(timezone.utc) - timedelta(minutes=minutes))
    series = c.list_time_series(request={"name": project, "filter": f'metric.type = "{metric_type}"', "interval": interval, "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL})
    values = []
    for s in series:
        for p in s.points:
            if hasattr(p.value, "double_value"):
                values.append(p.value.double_value)
    return {"points": len(values), "latest": values[-1] if values else None, "average": (sum(values) / len(values)) if values else None}
