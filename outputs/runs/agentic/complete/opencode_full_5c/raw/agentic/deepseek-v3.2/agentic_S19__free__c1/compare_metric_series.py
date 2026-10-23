import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2


def compare_metric_series(metric_name, filter_a, filter_b, window_minutes=60):
    """Compare metric values for two resources or dimension filters over the same window."""
    client = monitoring_v3.MetricServiceClient()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")
    project_name = f"projects/{project_id}"

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=window_minutes)

    interval = monitoring_v3.TimeInterval()
    interval.end_time = timestamp_pb2.Timestamp(seconds=int(end_time.timestamp()))
    interval.start_time = timestamp_pb2.Timestamp(seconds=int(start_time.timestamp()))

    def build_filter_string(filters):
        filter_parts = [f'metric.type = "{metric_name}"']
        for key, value in filters.items():
            if key.startswith("resource."):
                filter_parts.append(f'{key} = "{value}"')
            else:
                filter_parts.append(f'metric.labels.{key} = "{value}"')
        return " AND ".join(filter_parts)

    filter_a_str = build_filter_string(filter_a)
    filter_b_str = build_filter_string(filter_b)

    def fetch_series(filter_str):
        request = monitoring_v3.ListTimeSeriesRequest(
            name=project_name,
            filter=filter_str,
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        )

        series_data = []
        for time_series in client.list_time_series(request):
            for point in time_series.points:
                series_data.append(
                    {
                        "timestamp": point.interval.end_time.ToDatetime(),
                        "value": point.value.double_value
                        if point.value.HasField("double_value")
                        else point.value.int64_value,
                        "resource_labels": dict(time_series.resource.labels),
                    }
                )
        return series_data

    series_a = fetch_series(filter_a_str)
    series_b = fetch_series(filter_b_str)

    comparison = {
        "series_a": {
            "filter": filter_a,
            "data_points": len(series_a),
            "avg_value": sum(d["value"] for d in series_a) / len(series_a)
            if series_a
            else 0,
        },
        "series_b": {
            "filter": filter_b,
            "data_points": len(series_b),
            "avg_value": sum(d["value"] for d in series_b) / len(series_b)
            if series_b
            else 0,
        },
        "time_window": {"start": start_time, "end": end_time},
    }

    return comparison


if __name__ == "__main__":
    filter1 = {"resource.labels.zone": "us-central1-a"}
    filter2 = {"resource.labels.zone": "us-central1-b"}
    comparison = compare_metric_series(
        "compute.googleapis.com/instance/cpu/utilization", filter1, filter2, 120
    )
    print(f"Comparison result: {comparison}")
