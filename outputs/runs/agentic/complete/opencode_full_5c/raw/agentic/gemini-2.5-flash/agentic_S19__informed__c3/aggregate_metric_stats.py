import datetime
from google.cloud import monitoring_v3  # Provider-identifying signal
from observability_client import get_monitoring_client
from observability_models import MetricQuery, MetricResult


def aggregate_metric_stats(
    project_id: str,
    metric_type: str,
    end_time: datetime.datetime,
    start_time: datetime.datetime,
    aggregation_function: str = "mean",
    interval_minutes: int = 5,
) -> MetricResult:
    client = get_monitoring_client()
    project_name = f"projects/{project_id}"

    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(end_time.timestamp())},
        start_time={"seconds": int(start_time.timestamp())},
    )

    filter_str = f'metric.type = "{metric_type}"'

    # Convert aggregation_function string to the appropriate monitoring_v3.Aggregation.Aligner
    aligner_map = {
        "mean": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        "min": monitoring_v3.Aggregation.Aligner.ALIGN_MIN,
        "max": monitoring_v3.Aggregation.Aligner.ALIGN_MAX,
        "sum": monitoring_v3.Aggregation.Aligner.ALIGN_SUM,
        "count": monitoring_v3.Aggregation.Aligner.ALIGN_COUNT,
    }
    selected_aligner = aligner_map.get(
        aggregation_function.lower(), monitoring_v3.Aggregation.Aligner.ALIGN_MEAN
    )

    aggregation = monitoring_v3.Aggregation(
        alignment_period={"seconds": interval_minutes * 60},
        per_series_aligner=selected_aligner,
        group_by_fields=[
            "resource.label.instance_name",
            "metric.label.state",
        ],  # Example grouping fields
    )

    response = client.list_time_series(
        name=project_name,
        filter=filter_str,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=aggregation,
    )

    return MetricResult.from_response(response)
