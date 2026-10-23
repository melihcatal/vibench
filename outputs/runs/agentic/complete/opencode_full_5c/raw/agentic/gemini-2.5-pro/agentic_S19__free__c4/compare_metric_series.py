import time
from datetime import timedelta
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client
from observability_models import MetricQuery, MetricTimeSeries, TimeSeriesPoint
from typing import Dict, List


def _query_series(client, project_name, query: MetricQuery) -> List[MetricTimeSeries]:
    now = time.time()
    start_time = now - timedelta(minutes=query.minutes_ago).total_seconds()
    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": int(now)},
            "start_time": {"seconds": int(start_time)},
        }
    )

    filter_parts = [f'metric.type = "{query.metric_name}"']
    if query.filter_dimensions:
        for key, value in query.filter_dimensions.items():
            filter_parts.append(f'metric.labels.{key} = "{value}"')

    filter_str = " AND ".join(filter_parts)

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


def compare_metric_series(
    metric_name: str, minutes_ago: int, filter1: Dict[str, str], filter2: Dict[str, str]
) -> Dict[str, List[MetricTimeSeries]]:
    client, project_name = get_monitoring_client()

    query1 = MetricQuery(
        metric_name=metric_name, minutes_ago=minutes_ago, filter_dimensions=filter1
    )
    query2 = MetricQuery(
        metric_name=metric_name, minutes_ago=minutes_ago, filter_dimensions=filter2
    )

    series1 = _query_series(client, project_name, query1)
    series2 = _query_series(client, project_name, query2)

    return {"series1": series1, "series2": series2}
