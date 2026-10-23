import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2


def aggregate_metric_stats(
    metric_name, start_minutes_ago, end_minutes_ago, aggregation_alignment_period=300
):
    client = monitoring_v3.MetricServiceClient()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")

    now = datetime.utcnow()
    start_time = now - timedelta(minutes=start_minutes_ago)
    end_time = now - timedelta(minutes=end_minutes_ago)

    start_timestamp = timestamp_pb2.Timestamp()
    start_timestamp.FromDatetime(start_time)
    end_timestamp = timestamp_pb2.Timestamp()
    end_timestamp.FromDatetime(end_time)

    interval = monitoring_v3.TimeInterval(
        end_time=end_timestamp, start_time=start_timestamp
    )

    aggregation = monitoring_v3.Aggregation(
        alignment_period={"seconds": aggregation_alignment_period},
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
    )

    filter_str = f'metric.type = "{metric_name}"'

    request = monitoring_v3.ListTimeSeriesRequest(
        name=f"projects/{project_id}",
        filter=filter_str,
        interval=interval,
        aggregation=aggregation,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    stats = {
        "count": 0,
        "sum": 0.0,
        "min": float("inf"),
        "max": float("-inf"),
        "mean": 0.0,
    }

    values = []
    for time_series in client.list_time_series(request):
        for point in time_series.points:
            if point.value.HasField("double_value"):
                value = point.value.double_value
                values.append(value)
                stats["count"] += 1
                stats["sum"] += value
                stats["min"] = min(stats["min"], value)
                stats["max"] = max(stats["max"], value)

    if values:
        stats["mean"] = stats["sum"] / stats["count"]

    return stats
