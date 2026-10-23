from google.cloud import monitoring_v3
from observability_client import get_monitoring_client
from observability_models import MetricQueryRequest
import datetime
from typing import Dict, Any


def aggregate_metric_stats(request: MetricQueryRequest) -> Dict[str, Any]:
    client = get_monitoring_client()
    project_name = f"projects/{request.project_id}"

    interval = monitoring_v3.TimeInterval(
        start_time={
            "seconds": int(
                datetime.datetime.fromisoformat(
                    request.interval_start_time.replace("Z", "+00:00")
                ).timestamp()
            )
        },
        end_time={
            "seconds": int(
                datetime.datetime.fromisoformat(
                    request.interval_end_time.replace("Z", "+00:00")
                ).timestamp()
            )
        },
    )

    aggregation = monitoring_v3.Aggregation(
        alignment_period={"seconds": 60},  # 1 minute alignment
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,  # Default aligner
        cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,  # Default reducer
        group_by_fields=request.group_by_fields,
    )

    if request.aggregator == "SUM":
        aggregation.per_series_aligner = monitoring_v3.Aggregation.Aligner.ALIGN_SUM
        aggregation.cross_series_reducer = monitoring_v3.Aggregation.Reducer.REDUCE_SUM
    elif request.aggregator == "MIN":
        aggregation.per_series_aligner = monitoring_v3.Aggregation.Aligner.ALIGN_MIN
        aggregation.cross_series_reducer = monitoring_v3.Aggregation.Reducer.REDUCE_MIN
    elif request.aggregator == "MAX":
        aggregation.per_series_aligner = monitoring_v3.Aggregation.Aligner.ALIGN_MAX
        aggregation.cross_series_reducer = monitoring_v3.Aggregation.Reducer.REDUCE_MAX
    elif request.aggregator == "COUNT":
        aggregation.per_series_aligner = monitoring_v3.Aggregation.Aligner.ALIGN_COUNT
        aggregation.cross_series_reducer = (
            monitoring_v3.Aggregation.Reducer.REDUCE_COUNT
        )
    elif request.aggregator == "MEAN":
        aggregation.per_series_aligner = monitoring_v3.Aggregation.Aligner.ALIGN_MEAN
        aggregation.cross_series_reducer = monitoring_v3.Aggregation.Reducer.REDUCE_MEAN
    # Add more aggregators as needed

    query_filter = f'metric.type = "{request.metric_type}"'
    if request.filter_string:
        query_filter += f" AND {request.filter_string}"

    results = client.list_time_series(
        name=project_name,
        filter=query_filter,
        interval=interval,
        aggregation=aggregation,
    )

    aggregated_data = {}
    for series in results:
        if series.points:
            # For aggregated results, there's typically one point after cross_series_reducer
            point = series.points[0]
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

            key = (
                "_".join(f"{k}:{v}" for k, v in series.resource.labels.items())
                if series.resource.labels
                else "overall"
            )
            aggregated_data[key] = {
                "value": value,
                "time": point.interval.end_time.isoformat(),
            }
    return aggregated_data
