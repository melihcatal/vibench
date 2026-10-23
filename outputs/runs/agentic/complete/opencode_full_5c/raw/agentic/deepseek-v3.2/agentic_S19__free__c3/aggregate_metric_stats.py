import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2


def get_aggregated_metric_stats(metric_name, window_minutes=60):
    """Retrieve aggregated statistics for a metric over a time window."""
    client = monitoring_v3.MetricServiceClient()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")
    project_name = f"projects/{project_id}"

    interval = monitoring_v3.TimeInterval()
    now = datetime.utcnow()
    start_time = now - timedelta(minutes=window_minutes)

    start_timestamp = timestamp_pb2.Timestamp()
    start_timestamp.FromDatetime(start_time)
    end_timestamp = timestamp_pb2.Timestamp()
    end_timestamp.FromDatetime(now)

    interval.start_time = start_timestamp
    interval.end_time = end_timestamp

    filter_str = f'metric.type = "{metric_name}"'

    aggregation = monitoring_v3.Aggregation()
    aggregation.alignment_period = {"seconds": 300}
    aggregation.per_series_aligner = monitoring_v3.Aggregation.Aligner.ALIGN_MEAN

    try:
        results = client.list_time_series(
            request={
                "name": project_name,
                "filter": filter_str,
                "interval": interval,
                "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
                "aggregation": aggregation,
            }
        )

        all_values = []
        for series in results:
            for point in series.points:
                value = (
                    point.value.double_value
                    if point.value.double_value
                    else point.value.int64_value
                )
                if value is not None:
                    all_values.append(value)

        if not all_values:
            return {
                "count": 0,
                "min": None,
                "max": None,
                "avg": None,
                "sum": None,
                "metric": metric_name,
                "window_minutes": window_minutes,
            }

        return {
            "count": len(all_values),
            "min": min(all_values),
            "max": max(all_values),
            "avg": sum(all_values) / len(all_values),
            "sum": sum(all_values),
            "metric": metric_name,
            "window_minutes": window_minutes,
        }

    except Exception as e:
        print(f"Error aggregating metric {metric_name}: {e}")
        return {
            "count": 0,
            "min": None,
            "max": None,
            "avg": None,
            "sum": None,
            "metric": metric_name,
            "window_minutes": window_minutes,
        }
