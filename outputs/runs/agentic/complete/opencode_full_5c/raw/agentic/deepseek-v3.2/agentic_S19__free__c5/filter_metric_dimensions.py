import os
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2
import datetime


def filter_metric_dimensions(metric_name, dimension_filters, window_minutes=30):
    """Query metric data filtered by resource labels or dimensions."""
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

    filter_parts = [f'metric.type = "{metric_name}"']

    for key, value in dimension_filters.items():
        if key.startswith("resource."):
            filter_parts.append(f'resource.labels.{key[9:]} = "{value}"')
        else:
            filter_parts.append(f'metric.labels.{key} = "{value}"')

    filter_str = " AND ".join(filter_parts)

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": filter_str,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    filtered_data = []
    for series in results:
        series_info = {
            "metric_type": series.metric.type,
            "metric_labels": dict(series.metric.labels),
            "resource_type": series.resource.type,
            "resource_labels": dict(series.resource.labels),
            "points": [],
        }

        for point in series.points:
            series_info["points"].append(
                {
                    "timestamp": point.interval.end_time.ToDatetime().isoformat(),
                    "value": point.value.double_value
                    if point.value.HasField("double_value")
                    else point.value.int64_value,
                }
            )

        filtered_data.append(series_info)

    return filtered_data
