import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from google.cloud.monitoring_v3.services.metric_service import pagers

from observability_client import get_monitoring_client, get_project_id
from observability_models import QueryResult, TimeSeries, TimeSeriesPoint


def query_recent_metrics(metric_type: str, minutes: int = 60) -> QueryResult:
    client = get_monitoring_client()
    project_id = get_project_id()
    project_name = f"projects/{project_id}"

    now = datetime.utcnow()
    start_time = now - timedelta(minutes=minutes)

    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": int(now.timestamp())},
            "start_time": {"seconds": int(start_time.timestamp())},
        }
    )

    request = {
        "name": project_name,
        "filter": f'metric.type = "{metric_type}"',
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    }

    results: pagers.ListTimeSeriesPager = client.list_time_series(request)

    query_result = QueryResult()
    for result in results:
        ts = TimeSeries(
            metric_name=result.metric.type, resource_labels=dict(result.resource.labels)
        )
        for point in result.points:
            ts.points.append(
                TimeSeriesPoint(
                    timestamp=point.interval.end_time.timestamp(),
                    value=point.value.double_value,
                )
            )
        query_result.series.append(ts)

    return query_result
