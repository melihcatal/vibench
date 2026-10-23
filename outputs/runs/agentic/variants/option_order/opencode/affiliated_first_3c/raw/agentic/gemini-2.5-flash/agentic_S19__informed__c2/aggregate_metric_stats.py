from datetime import datetime
from typing import List, Optional
import os

from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.duration_pb2 import Duration

from observability_client import get_monitoring_client
from observability_models import MetricQueryRequest, MetricAggregationResult


def aggregate_metric_stats(
    request: MetricQueryRequest,
) -> List[MetricAggregationResult]:
    client = get_monitoring_client()

    end_timestamp = Timestamp()
    end_timestamp.FromDatetime(request.end_time)
    start_timestamp = Timestamp()
    start_timestamp.FromDatetime(request.start_time)

    interval = monitoring_v3.TimeInterval(
        end_time=end_timestamp,
        start_time=start_timestamp,
    )

    aggregation = monitoring_v3.Aggregation(
        alignment_period=Duration(
            seconds=int((request.end_time - request.start_time).total_seconds())
        ),
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
        group_by_fields=[
            "metric.labels.instance_name",
            "resource.labels.instance_id",
        ],  # Example grouping
    )

    query_filter = f'metric.type = "{request.metric_type}"'
    if request.filter_str:
        query_filter += f" AND {request.filter_str}"

    results = client.list_time_series(
        name=f"projects/{request.project_id}",
        filter=query_filter,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=aggregation,
    )

    aggregation_results: List[MetricAggregationResult] = []
    for time_series in results:
        mean_value: Optional[float] = None
        if time_series.points:
            # For REDUCE_MEAN, there should be one point with the aggregated value
            point = time_series.points[0]
            mean_value = (
                point.value.double_value
                if point.value.HasField("double_value")
                else None
            )

        labels = {k: v for k, v in time_series.metric.labels.items()}
        labels.update({k: v for k, v in time_series.resource.labels.items()})

        aggregation_results.append(
            MetricAggregationResult(
                metric_type=request.metric_type, mean=mean_value, labels=labels
            )
        )

    return aggregation_results
