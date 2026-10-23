import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2


def query_metric_with_dimension_filters(
    metric_name, dimension_filters, window_minutes=30
):
    """Query metric data filtered by resource labels or dimensions."""
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

    filter_parts = [f'metric.type = "{metric_name}"']

    for key, value in dimension_filters.items():
        if key.startswith("resource."):
            filter_parts.append(f'{key} = "{value}"')
        else:
            filter_parts.append(f'metric.labels.{key} = "{value}"')

    filter_str = " AND ".join(filter_parts)

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

        filtered_data = []
        for series in results:
            series_data = {
                "metric_type": series.metric.type,
                "metric_labels": dict(series.metric.labels),
                "resource_labels": dict(series.resource.labels),
                "points": [],
            }

            for point in series.points:
                series_data["points"].append(
                    {
                        "timestamp": point.interval.end_time.ToDatetime(),
                        "value": point.value.double_value
                        if point.value.double_value
                        else point.value.int64_value,
                    }
                )

            filtered_data.append(series_data)

        return filtered_data

    except Exception as e:
        print(f"Error querying metric with filters: {e}")
        return []
