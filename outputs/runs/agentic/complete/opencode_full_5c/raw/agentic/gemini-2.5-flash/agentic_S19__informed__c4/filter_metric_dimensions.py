from datetime import datetime
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client
from observability_models import (
    MetricQueryRequest,
    MetricQueryResult,
    MetricQueryResponse,
)


def filter_metric_dimensions(request: MetricQueryRequest) -> MetricQueryResponse:
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

    query_filter = f'metric.type = "{request.metric_type}" '
    if request.filter_string:
        query_filter += f"AND {request.filter_string}"

    results = []
    for response in client.list_time_series(
        name=project_name,
        filter=query_filter,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    ):
        for series in response.time_series:
            for point in series.points:
                results.append(
                    MetricQueryResult(
                        time=point.interval.end_time.isoformat(),
                        value=point.value.double_value or point.value.int64_value,
                        labels={**series.metric.labels, **series.resource.labels},
                    )
                )

    return MetricQueryResponse(metric_data=results)
