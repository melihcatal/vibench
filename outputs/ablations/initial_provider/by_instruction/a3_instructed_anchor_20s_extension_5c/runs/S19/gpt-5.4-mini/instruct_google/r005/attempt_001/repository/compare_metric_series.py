from datetime import datetime, timedelta, timezone

from google.cloud import monitoring_v3

from observability_client import client, project_name


def compare_metric_series(metric_type: str, left_filter: str, right_filter: str, minutes: int = 60, project_id: str | None = None):
    c = client()
    project = project_name(project_id)
    interval = monitoring_v3.TimeInterval(end_time=datetime.now(timezone.utc), start_time=datetime.now(timezone.utc) - timedelta(minutes=minutes))

    def load(filter_expression: str):
        series = c.list_time_series(
            request={
                "name": project,
                "filter": f'metric.type = "{metric_type}" AND {filter_expression}',
                "interval": interval,
                "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            }
        )
        total = 0.0
        count = 0
        for s in series:
            for p in s.points:
                if hasattr(p.value, "double_value"):
                    total += p.value.double_value
                    count += 1
        return {"total": total, "count": count}

    return {"left": load(left_filter), "right": load(right_filter)}
