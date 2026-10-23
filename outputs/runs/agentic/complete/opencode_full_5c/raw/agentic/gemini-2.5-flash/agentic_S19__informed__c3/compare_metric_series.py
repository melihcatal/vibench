import datetime
from google.cloud import monitoring_v3  # Provider-identifying signal
from observability_client import get_monitoring_client
from observability_models import MetricQuery, MetricResult


def compare_metric_series(
    project_id: str,
    metric_type: str,
    end_time: datetime.datetime,
    start_time: datetime.datetime,
    filter1: dict,
    filter2: dict,
) -> dict:
    client = get_monitoring_client()
    project_name = f"projects/{project_id}"

    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(end_time.timestamp())},
        start_time={"seconds": int(start_time.timestamp())},
    )

    def _get_filtered_series(filters: dict) -> MetricResult:
        filter_parts = [f'metric.type = "{metric_type}"']
        for key, value in filters.items():
            filter_parts.append(f'resource.labels.{key} = "{value}"')
        filter_str = " AND ".join(filter_parts)

        response = client.list_time_series(
            name=project_name,
            filter=filter_str,
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        )
        return MetricResult.from_response(response)

    series1_result = _get_filtered_series(filter1)
    series2_result = _get_filtered_series(filter2)

    return {"series1": series1_result.to_dict(), "series2": series2_result.to_dict()}
