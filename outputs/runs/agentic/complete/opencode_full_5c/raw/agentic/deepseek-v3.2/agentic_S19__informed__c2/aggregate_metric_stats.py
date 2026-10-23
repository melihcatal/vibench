import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2


def get_aggregated_metric_stats(
    metric_name, aggregation_period_minutes=5, window_minutes=60
):
    client = monitoring_v3.MetricServiceClient()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    interval = monitoring_v3.TimeInterval()
    now = datetime.utcnow()
    start_time = now - timedelta(minutes=window_minutes)

    start_timestamp = timestamp_pb2.Timestamp()
    start_timestamp.FromDatetime(start_time)
    end_timestamp = timestamp_pb2.Timestamp()
    end_timestamp.FromDatetime(now)

    interval.start_time = start_timestamp
    interval.end_time = end_timestamp

    aggregation = monitoring_v3.Aggregation()
    aggregation.alignment_period.seconds = aggregation_period_minutes * 60
    aggregation.per_series_aligner = monitoring_v3.Aggregation.Aligner.ALIGN_MEAN
    aggregation.cross_series_reducer = monitoring_v3.Aggregation.Reducer.REDUCE_MEAN

    filter_str = f'metric.type = "{metric_name}"'

    request = monitoring_v3.ListTimeSeriesRequest(
        name=f"projects/{project_id}",
        filter=filter_str,
        interval=interval,
        aggregation=aggregation,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    results = client.list_time_series(request)

    aggregated_stats = []
    for series in results:
        if series.points:
            values = []
            for point in series.points:
                value = (
                    point.value.double_value
                    if point.value.HasField("double_value")
                    else point.value.int64_value
                )
                values.append(value)

            if values:
                aggregated_stats.append(
                    {
                        "metric_type": series.metric.type,
                        "metric_labels": dict(series.metric.labels),
                        "resource_type": series.resource.type,
                        "resource_labels": dict(series.resource.labels),
                        "mean": sum(values) / len(values),
                        "min": min(values),
                        "max": max(values),
                        "count": len(values),
                        "aggregation_period_minutes": aggregation_period_minutes,
                    }
                )

    return aggregated_stats


if __name__ == "__main__":
    stats = get_aggregated_metric_stats(
        "compute.googleapis.com/instance/disk/read_bytes_count", 5, 60
    )
    for stat in stats:
        print(
            f"Metric: {stat['metric_type']}, Mean: {stat['mean']:.2f}, Min: {stat['min']:.2f}, Max: {stat['max']:.2f}"
        )
