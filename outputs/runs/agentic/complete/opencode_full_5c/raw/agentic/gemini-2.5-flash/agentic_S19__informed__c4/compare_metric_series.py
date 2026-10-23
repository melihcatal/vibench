from datetime import datetime
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client
from observability_models import (
    MetricQueryRequest,
    MetricQueryResult,
    MetricQueryResponse,
)
from typing import Tuple


def compare_metric_series(
    request: MetricQueryRequest, filter_string_2: str
) -> Tuple[MetricQueryResponse, MetricQueryResponse]:
    client = get_monitoring_client()
    project_name = f"projects/{request.project_id}"

    interval = monitoring_v3.TimeInterval(
        end_time={
            "seconds": int(
                datetime.fromisoformat(
                    request.end_time.replace("Z", "+00:00")
                ).timestamp()
            )
        },
        start_time={
            "seconds": int(
                datetime.fromisoformat(
                    request.start_time.replace("Z", "+00:00")
                ).timestamp()
            )
        },
    )

    # First series
    query_filter_1 = f'metric.type = "{request.metric_type}" '
    if request.filter_string:
        query_filter_1 += f"AND {request.filter_string}"

    results_1 = []
    for response in client.list_time_series(
        name=project_name,
        filter=query_filter_1,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    ):
        for series in response.time_series:
            for point in series.points:
                results_1.append(
                    MetricQueryResult(
                        time=point.interval.end_time.isoformat(),
                        value=point.value.double_value or point.value.int64_value,
                        labels={**series.metric.labels, **series.resource.labels},
                    )
                )
    response_1 = MetricQueryResponse(metric_data=results_1)

    # Second series
    query_filter_2 = f'metric.type = "{request.metric_type}" '
    if filter_string_2:
        query_filter_2 += f"AND {filter_string_2}"

    results_2 = []
    for response in client.list_time_series(
        name=project_name,
        filter=query_filter_2,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    ):
        for series in response.time_series:
            for point in series.points:
                results_2.append(
                    MetricQueryResult(
                        time=point.interval.end_time.isoformat(),
                        value=point.value.double_value or point.value.int64_value,
                        labels={**series.metric.labels, **series.resource.labels},
                    )
                )
    response_2 = MetricQueryResponse(metric_data=results_2)

    return response_1, response_2
