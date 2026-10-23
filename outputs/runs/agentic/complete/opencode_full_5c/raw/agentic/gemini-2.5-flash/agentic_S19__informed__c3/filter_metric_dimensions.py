import datetime
from google.cloud import monitoring_v3  # Provider-identifying signal
from observability_client import get_monitoring_client
from observability_models import MetricQuery, MetricResult


def filter_metric_dimensions(
    project_id: str,
    metric_type: str,
    end_time: datetime.datetime,
    start_time: datetime.datetime,
    dimension_filters: dict,
) -> MetricResult:
    client = get_monitoring_client()
    project_name = f"projects/{project_id}"

    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(end_time.timestamp())},
        start_time={"seconds": int(start_time.timestamp())},
    )

    filter_parts = [f'metric.type = "{metric_type}"']
    for key, value in dimension_filters.items():
        filter_parts.append(f'resource.labels.{key} = "{value}"')
    filter_str = " AND ".join(filter_parts)

    response = client.list_time_series(
        name=project_name,
        filter=filter_str,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    return MetricResult.from_response(response)
