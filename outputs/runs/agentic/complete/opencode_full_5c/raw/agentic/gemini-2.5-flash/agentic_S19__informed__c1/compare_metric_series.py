from datetime import datetime, timedelta
from typing import List, Dict, Any
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client
from observability_models import (
    MetricQuery,
    MetricDataPoint,
    MetricSeries,
    MetricResponse,
)


def compare_metric_series(
    query1: MetricQuery, query2: MetricQuery
) -> Dict[str, MetricResponse]:
    client = get_monitoring_client()
    project_name = f"projects/{query1.project_id}"

    # Query 1
    interval1 = monitoring_v3.TimeInterval()
    interval1.end_time.FromDatetime(
        datetime.strptime(query1.end_time, "%Y-%m-%dT%H:%M:%SZ")
    )
    interval1.start_time.FromDatetime(
        datetime.strptime(query1.start_time, "%Y-%m-%dT%H:%M:%SZ")
    )

    metric_filter1 = f'metric.type="{query1.metric_type}"'
    if query1.filter:
        metric_filter1 += f" AND {query1.filter}"

    results1 = client.list_time_series(
        name=project_name,
        filter=metric_filter1,
        interval=interval1,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    all_metric_series1 = []
    for series in results1:
        points = []
        for point in series.points:
            point_value = None
            if point.value.double_value is not None:
                point_value = point.value.double_value
            elif point.value.int64_value is not None:
                point_value = point.value.int64_value
            elif point.value.string_value is not None:
                point_value = point.value.string_value
            elif point.value.bool_value is not None:
                point_value = point.value.bool_value

            points.append(
                MetricDataPoint(
                    value=point_value, timestamp=point.interval.end_time.isoformat()
                )
            )
        all_metric_series1.append(
            MetricSeries(
                resource_labels=dict(series.resource.labels),
                metric_labels=dict(series.metric.labels),
                points=points,
            )
        )
    response1 = MetricResponse(metric_series=all_metric_series1)

    # Query 2
    interval2 = monitoring_v3.TimeInterval()
    interval2.end_time.FromDatetime(
        datetime.strptime(query2.end_time, "%Y-%m-%dT%H:%M:%SZ")
    )
    interval2.start_time.FromDatetime(
        datetime.strptime(query2.start_time, "%Y-%m-%dT%H:%M:%SZ")
    )

    metric_filter2 = f'metric.type="{query2.metric_type}"'
    if query2.filter:
        metric_filter2 += f" AND {query2.filter}"

    results2 = client.list_time_series(
        name=project_name,
        filter=metric_filter2,
        interval=interval2,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    all_metric_series2 = []
    for series in results2:
        points = []
        for point in series.points:
            point_value = None
            if point.value.double_value is not None:
                point_value = point.value.double_value
            elif point.value.int64_value is not None:
                point_value = point.value.int64_value
            elif point.value.string_value is not None:
                point_value = point.value.string_value
            elif point.value.bool_value is not None:
                point_value = point.value.bool_value

            points.append(
                MetricDataPoint(
                    value=point_value, timestamp=point.interval.end_time.isoformat()
                )
            )
        all_metric_series2.append(
            MetricSeries(
                resource_labels=dict(series.resource.labels),
                metric_labels=dict(series.metric.labels),
                points=points,
            )
        )
    response2 = MetricResponse(metric_series=all_metric_series2)

    return {"series1": response1, "series2": response2}
