import os
from datetime import datetime, timedelta, timezone

from google.cloud import monitoring_v3

from observability_client import client, project_name
from observability_models import MetricWindow, normalize_timestamp, normalize_value


def query_metric_window(metric_type: str, minutes: int = 60, project_id: str | None = None):
    c = client()
    project = project_name(project_id)
    interval = monitoring_v3.TimeInterval(
        end_time=datetime.now(timezone.utc),
        start_time=datetime.now(timezone.utc) - timedelta(minutes=minutes),
    )
    results = c.list_time_series(
        request={
            "name": project,
            "filter": f'metric.type = "{metric_type}"',
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )
    points = []
    for series in results:
        for point in series.points:
            points.append(
                {
                    "timestamp": normalize_timestamp(point.interval.end_time),
                    "value": normalize_value(point.value),
                    "resource_type": series.resource.type,
                }
            )
    return points


if __name__ == "__main__":
    metric = os.environ.get("METRIC_TYPE", "compute.googleapis.com/instance/cpu/utilization")
    print(query_metric_window(metric))
