from datetime import datetime, timedelta, timezone

from google.cloud import monitoring_v3

from observability_client import client, project_name


def filter_metric_dimensions(metric_type: str, dimension_filter: str, minutes: int = 60, project_id: str | None = None):
    c = client()
    project = project_name(project_id)
    interval = monitoring_v3.TimeInterval(end_time=datetime.now(timezone.utc), start_time=datetime.now(timezone.utc) - timedelta(minutes=minutes))
    return list(
        c.list_time_series(
            request={
                "name": project,
                "filter": f'metric.type = "{metric_type}" AND {dimension_filter}',
                "interval": interval,
                "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            }
        )
    )
