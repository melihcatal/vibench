from google.cloud import monitoring_v3
from observability_client import get_monitoring_client
from observability_models import MetricQueryRequest, MetricSeries, MetricPoint
import datetime
from typing import List, Dict


def _fetch_series(
    client: monitoring_v3.MetricServiceClient,
    project_id: str,
    metric_type: str,
    interval: monitoring_v3.TimeInterval,
    filter_string: str,
) -> List[MetricSeries]:
    project_name = f"projects/{project_id}"
    query_filter = f'metric.type = "{metric_type}" AND {filter_string}'

    results = client.list_time_series(
        name=project_name,
        filter=query_filter,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    metric_series_list = []
    for series in results:
        points = []
        for point in series.points:
            value = (
                point.value.double_value
                if point.value.HasField("double_value")
                else None
            )
            if point.value.HasField("int64_value"):
                value = point.value.int64_value
            elif point.value.HasField("bool_value"):
                value = point.value.bool_value
            elif point.value.HasField("string_value"):
                value = point.value.string_value
            points.append(
                MetricPoint(time=point.interval.end_time.isoformat(), value=value)
            )
        metric_series_list.append(
            MetricSeries(
                resource_labels=dict(series.resource.labels),
                metric_labels=dict(series.metric.labels),
                points=points,
            )
        )
    return metric_series_list


def compare_metric_series(
    request_series1: MetricQueryRequest, request_series2: MetricQueryRequest
) -> Dict[str, List[MetricSeries]]:
    client = get_monitoring_client()

    interval = monitoring_v3.TimeInterval(
        start_time={
            "seconds": int(
                datetime.datetime.fromisoformat(
                    request_series1.interval_start_time.replace("Z", "+00:00")
                ).timestamp()
            )
        },
        end_time={
            "seconds": int(
                datetime.datetime.fromisoformat(
                    request_series1.interval_end_time.replace("Z", "+00:00")
                ).timestamp()
            )
        },
    )

    series1_data = _fetch_series(
        client,
        request_series1.project_id,
        request_series1.metric_type,
        interval,
        request_series1.filter_string,
    )
    series2_data = _fetch_series(
        client,
        request_series2.project_id,
        request_series2.metric_type,
        interval,
        request_series2.filter_string,
    )

    return {"series1": series1_data, "series2": series2_data}
