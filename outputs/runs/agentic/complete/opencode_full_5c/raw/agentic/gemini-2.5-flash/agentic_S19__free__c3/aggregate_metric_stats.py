import os
from datetime import datetime, timedelta
from google.protobuf.timestamp_pb2 import Timestamp
from observability_client import ObservabilityClient
from observability_models import MetricAggregate
from google.cloud import monitoring_v3


def aggregate_metric_stats(
    project_id: str,
    metric_type: str,
    end_time: datetime,
    start_time: datetime,
    reducer: monitoring_v3.Aggregation.Aligner,
) -> MetricAggregate:
    client = ObservabilityClient(project_id).get_monitoring_client()
    project_name = f"projects/{project_id}"

    interval = monitoring_v3.TimeInterval(
        end_time=Timestamp(seconds=int(end_time.timestamp())),
        start_time=Timestamp(seconds=int(start_time.timestamp())),
    )

    aggregation = monitoring_v3.Aggregation(
        alignment_period=Timestamp(seconds=60),
        per_series_aligner=reducer,
        cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_NONE,
        group_by_fields=[
            "resource.type",
            "resource.labels.instance_id",
        ],  # Example grouping
    )

    query_params = {
        "name": project_name,
        "filter": f'metric.type = "{metric_type}"',
        "interval": interval,
        "aggregation": aggregation,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    }

    response = client.list_time_series(**query_params)

    # For simplicity, we'll take the first time series and its last point's value.
    # A real-world scenario might involve more complex aggregation of multiple series.
    if response.time_series and response.time_series[0].points:
        ts = response.time_series[0]
        last_point_value = getattr(
            ts.points[-1].value, ts.points[-1].value.WhichOneof("value_type")
        )
        return MetricAggregate(
            metric_type=metric_type,
            resource_labels=dict(ts.resource.labels),
            reducer=reducer.name,  # Use name for easier representation
            value=last_point_value,
        )
    return MetricAggregate(
        metric_type=metric_type, resource_labels={}, reducer=reducer.name, value=None
    )
