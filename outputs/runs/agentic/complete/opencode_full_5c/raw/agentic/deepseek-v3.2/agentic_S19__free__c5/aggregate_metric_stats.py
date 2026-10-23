import os
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2
import datetime
import statistics


def aggregate_metric_stats(metric_name, window_minutes=60, aggregation="avg"):
    """Retrieve aggregated statistics for a metric over a time window."""
    client = monitoring_v3.MetricServiceClient()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")
    project_name = f"projects/{project_id}"

    end_time = datetime.datetime.now(datetime.timezone.utc)
    start_time = end_time - datetime.timedelta(minutes=window_minutes)

    end_timestamp = timestamp_pb2.Timestamp()
    end_timestamp.FromDatetime(end_time)
    start_timestamp = timestamp_pb2.Timestamp()
    start_timestamp.FromDatetime(start_time)

    interval = monitoring_v3.TimeInterval(
        end_time=end_timestamp, start_time=start_timestamp
    )

    aggregation_obj = monitoring_v3.Aggregation()
    if aggregation == "avg":
        aggregation_obj.alignment_period = {"seconds": 300}
        aggregation_obj.per_series_aligner = (
            monitoring_v3.Aggregation.Aligner.ALIGN_MEAN
        )
        aggregation_obj.cross_series_reducer = (
            monitoring_v3.Aggregation.Reducer.REDUCE_MEAN
        )
    elif aggregation == "max":
        aggregation_obj.alignment_period = {"seconds": 300}
        aggregation_obj.per_series_aligner = monitoring_v3.Aggregation.Aligner.ALIGN_MAX
        aggregation_obj.cross_series_reducer = (
            monitoring_v3.Aggregation.Reducer.REDUCE_MAX
        )
    elif aggregation == "min":
        aggregation_obj.alignment_period = {"seconds": 300}
        aggregation_obj.per_series_aligner = monitoring_v3.Aggregation.Aligner.ALIGN_MIN
        aggregation_obj.cross_series_reducer = (
            monitoring_v3.Aggregation.Reducer.REDUCE_MIN
        )
    elif aggregation == "sum":
        aggregation_obj.alignment_period = {"seconds": 300}
        aggregation_obj.per_series_aligner = monitoring_v3.Aggregation.Aligner.ALIGN_SUM
        aggregation_obj.cross_series_reducer = (
            monitoring_v3.Aggregation.Reducer.REDUCE_SUM
        )
    else:
        aggregation_obj.alignment_period = {"seconds": 300}
        aggregation_obj.per_series_aligner = (
            monitoring_v3.Aggregation.Aligner.ALIGN_MEAN
        )
        aggregation_obj.cross_series_reducer = (
            monitoring_v3.Aggregation.Reducer.REDUCE_MEAN
        )

    filter_str = f'metric.type = "{metric_name}"'

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": filter_str,
            "interval": interval,
            "aggregation": aggregation_obj,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    stats = {
        "metric": metric_name,
        "window_minutes": window_minutes,
        "aggregation": aggregation,
        "series_count": 0,
        "datapoint_count": 0,
        "values": [],
    }

    for series in results:
        stats["series_count"] += 1
        for point in series.points:
            stats["datapoint_count"] += 1
            value = (
                point.value.double_value
                if point.value.HasField("double_value")
                else point.value.int64_value
            )
            stats["values"].append(value)

    if stats["values"]:
        stats["mean"] = statistics.mean(stats["values"])
        stats["median"] = statistics.median(stats["values"])
        stats["min"] = min(stats["values"])
        stats["max"] = max(stats["values"])
        if len(stats["values"]) > 1:
            stats["stdev"] = statistics.stdev(stats["values"])
        else:
            stats["stdev"] = 0

    return stats
