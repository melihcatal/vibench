import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2


def compare_metric_series(metric_name, filter_a, filter_b, window_minutes=60):
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

    def build_filter_string(base_filter):
        filter_parts = [f'metric.type = "{metric_name}"']
        for key, value in base_filter.items():
            if key.startswith("metric."):
                filter_parts.append(f'{key} = "{value}"')
            elif key.startswith("resource."):
                filter_parts.append(f'{key} = "{value}"')
            else:
                filter_parts.append(f'metric.labels.{key} = "{value}"')
        return " AND ".join(filter_parts)

    filter_a_str = build_filter_string(filter_a)
    filter_b_str = build_filter_string(filter_b)

    def fetch_series(filter_str):
        request = monitoring_v3.ListTimeSeriesRequest(
            name=f"projects/{project_id}",
            filter=filter_str,
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        )
        results = client.list_time_series(request)

        series_data = []
        for series in results:
            values = []
            for point in series.points:
                value = (
                    point.value.double_value
                    if point.value.HasField("double_value")
                    else point.value.int64_value
                )
                values.append(value)

            if values:
                series_data.append(
                    {
                        "metric_labels": dict(series.metric.labels),
                        "resource_labels": dict(series.resource.labels),
                        "values": values,
                        "mean": sum(values) / len(values) if values else 0,
                        "min": min(values) if values else 0,
                        "max": max(values) if values else 0,
                        "count": len(values),
                    }
                )
        return series_data

    series_a = fetch_series(filter_a_str)
    series_b = fetch_series(filter_b_str)

    comparison_results = {"series_a": series_a, "series_b": series_b, "comparison": []}

    if series_a and series_b:
        mean_a = series_a[0]["mean"] if series_a else 0
        mean_b = series_b[0]["mean"] if series_b else 0

        comparison_results["comparison"].append(
            {
                "metric": metric_name,
                "mean_difference": mean_b - mean_a,
                "percent_difference": ((mean_b - mean_a) / mean_a * 100)
                if mean_a != 0
                else float("inf"),
                "window_minutes": window_minutes,
            }
        )

    return comparison_results


if __name__ == "__main__":
    filter_a = {"resource.labels.instance_id": "instance-1"}
    filter_b = {"resource.labels.instance_id": "instance-2"}
    comparison = compare_metric_series(
        "compute.googleapis.com/instance/cpu/utilization", filter_a, filter_b, 30
    )
    print(f"Comparison results: {comparison['comparison']}")
