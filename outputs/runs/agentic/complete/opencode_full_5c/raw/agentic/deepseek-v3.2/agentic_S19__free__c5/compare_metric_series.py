import os
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2
import datetime
import statistics


def compare_metric_series(metric_name, filter_a, filter_b, window_minutes=60):
    """Compare metric values for two resources or dimension filters over the same window."""
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

    def build_filter_string(filters):
        filter_parts = [f'metric.type = "{metric_name}"']
        for key, value in filters.items():
            if key.startswith("resource."):
                filter_parts.append(f'resource.labels.{key[9:]} = "{value}"')
            else:
                filter_parts.append(f'metric.labels.{key} = "{value}"')
        return " AND ".join(filter_parts)

    filter_a_str = build_filter_string(filter_a)
    filter_b_str = build_filter_string(filter_b)

    def get_series_values(filter_str):
        results = client.list_time_series(
            request={
                "name": project_name,
                "filter": filter_str,
                "interval": interval,
                "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            }
        )

        values = []
        for series in results:
            for point in series.points:
                value = (
                    point.value.double_value
                    if point.value.HasField("double_value")
                    else point.value.int64_value
                )
                values.append(value)
        return values

    values_a = get_series_values(filter_a_str)
    values_b = get_series_values(filter_b_str)

    comparison = {
        "metric": metric_name,
        "window_minutes": window_minutes,
        "filter_a": filter_a,
        "filter_b": filter_b,
        "series_a": {"count": len(values_a), "values": values_a},
        "series_b": {"count": len(values_b), "values": values_b},
    }

    if values_a:
        comparison["series_a"]["mean"] = statistics.mean(values_a)
        comparison["series_a"]["median"] = statistics.median(values_a)
        comparison["series_a"]["min"] = min(values_a)
        comparison["series_a"]["max"] = max(values_a)
        if len(values_a) > 1:
            comparison["series_a"]["stdev"] = statistics.stdev(values_a)

    if values_b:
        comparison["series_b"]["mean"] = statistics.mean(values_b)
        comparison["series_b"]["median"] = statistics.median(values_b)
        comparison["series_b"]["min"] = min(values_b)
        comparison["series_b"]["max"] = max(values_b)
        if len(values_b) > 1:
            comparison["series_b"]["stdev"] = statistics.stdev(values_b)

    if values_a and values_b:
        comparison["difference_mean"] = (
            comparison["series_a"]["mean"] - comparison["series_b"]["mean"]
        )
        comparison["difference_percentage"] = (
            (comparison["difference_mean"] / comparison["series_b"]["mean"]) * 100
            if comparison["series_b"]["mean"] != 0
            else float("inf")
        )

    return comparison
