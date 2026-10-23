from datetime import datetime, timedelta
from observability_client import ObservabilityClient
from observability_models import normalize_time_series
from google.cloud import monitoring_v3


def aggregate_metric_stats(
    metric_name: str,
    end_time: datetime,
    minutes: int,
    aggregation_function: str = "mean",
) -> list:
    client = ObservabilityClient()
    monitoring_client = client.get_monitoring_client()
    project_name = client.get_project_name()

    start_time = end_time - timedelta(minutes=minutes)

    interval = monitoring_v3.TimeInterval(
        end_time=end_time.isoformat() + "Z",
        start_time=start_time.isoformat() + "Z",
    )

    query_filter = f'metric.type = "{metric_name}"'

    # Define aggregation parameters
    # The available aggregation functions depend on the metric kind and value type.
    # Common ones include REDUCE_MEAN, REDUCE_MAX, REDUCE_MIN, REDUCE_SUM, REDUCE_COUNT
    if aggregation_function == "mean":
        agg_reducer = monitoring_v3.Aggregation.Reducer.REDUCE_MEAN
    elif aggregation_function == "max":
        agg_reducer = monitoring_v3.Aggregation.Reducer.REDUCE_MAX
    elif aggregation_function == "min":
        agg_reducer = monitoring_v3.Aggregation.Reducer.REDUCE_MIN
    elif aggregation_function == "sum":
        agg_reducer = monitoring_v3.Aggregation.Reducer.REDUCE_SUM
    elif aggregation_function == "count":
        agg_reducer = monitoring_v3.Aggregation.Reducer.REDUCE_COUNT
    else:
        raise ValueError("Unsupported aggregation function")

    aggregation = monitoring_v3.Aggregation(
        alignment_period={
            "seconds": 60 * minutes
        },  # Align to the whole window for a single aggregate stat
        per_series_reducer=agg_reducer,
        group_by_fields=[
            "metric.type",
            "resource.type",
        ],  # Group by metric and resource type to get one aggregate
    )

    response = monitoring_client.list_time_series(
        name=project_name,
        filter=query_filter,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=aggregation,
    )

    return normalize_time_series([series.to_dict() for series in response])
