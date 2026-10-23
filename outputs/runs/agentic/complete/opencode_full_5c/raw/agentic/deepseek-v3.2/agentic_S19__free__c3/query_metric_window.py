import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2


def query_recent_metric_data(metric_name, window_minutes=30):
    """Query recent datapoints for a named metric over a time window."""
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
    aggregation.alignment_period = {"seconds": 60}
    aggregation.per_series_aligner = monitoring_v3.Aggregation.Aligner.ALIGN_MEAN
    aggregation.cross_series_reducer = monitoring_v3.Aggregation.Reducer.REDUCE_NONE

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

        datapoints = []
        for series in results:
            for point in series.points:
                datapoints.append(
                    {
                        "timestamp": point.interval.end_time.ToDatetime(),
                        "value": point.value.double_value
                        if point.value.double_value
                        else point.value.int64_value,
                        "metric_type": series.metric.type,
                        "resource_labels": dict(series.resource.labels),
                    }
                )

        return datapoints

    except Exception as e:
        print(f"Error querying metric {metric_name}: {e}")
        return []
