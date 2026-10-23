import time
from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client
from observability_models import MetricQuery, MetricTimeSeries, TimeSeriesPoint


def query_metric_window(query: MetricQuery) -> list[MetricTimeSeries]:
    client, project_name = get_monitoring_client()

    now = time.time()
    seconds = now - timedelta(minutes=query.minutes_ago).total_seconds()
    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": int(now)},
            "start_time": {"seconds": int(seconds)},
        }
    )

    filter_str = f'metric.type = "{query.metric_name}"'

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": filter_str,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    series_list = []
    for result in results:
        points = []
        for point in result.points:
            points.append(
                TimeSeriesPoint(
                    timestamp=point.interval.end_time.timestamp(),
                    value=point.value.double_value,
                )
            )
        series_list.append(
            MetricTimeSeries(
                metric_name=result.metric.type,
                points=points,
                dimensions=dict(result.metric.labels),
            )
        )
    return series_list
