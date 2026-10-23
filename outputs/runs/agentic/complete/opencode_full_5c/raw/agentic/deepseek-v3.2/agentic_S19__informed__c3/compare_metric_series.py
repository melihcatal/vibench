import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2


def compare_metric_series(
    metric_name, filter_a, filter_b, start_minutes_ago, end_minutes_ago
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

    def query_with_filter(dimension_filter):
        filter_parts = [f'metric.type = "{metric_name}"']
        for key, value in dimension_filter.items():
            filter_parts.append(f'metric.labels.{key} = "{value}"')

        filter_str = " AND ".join(filter_parts)

        request = monitoring_v3.ListTimeSeriesRequest(
            name=f"projects/{project_id}",
            filter=filter_str,
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        )

        values = []
        for time_series in client.list_time_series(request):
            for point in time_series.points:
                if point.value.HasField("double_value"):
                    values.append(point.value.double_value)
        return values

    values_a = query_with_filter(filter_a)
    values_b = query_with_filter(filter_b)

    comparison = {
        "series_a": {
            "count": len(values_a),
            "mean": sum(values_a) / len(values_a) if values_a else 0,
            "min": min(values_a) if values_a else 0,
            "max": max(values_a) if values_a else 0,
        },
        "series_b": {
            "count": len(values_b),
            "mean": sum(values_b) / len(values_b) if values_b else 0,
            "min": min(values_b) if values_b else 0,
            "max": max(values_b) if values_b else 0,
        },
        "difference": {
            "mean_diff": (sum(values_a) / len(values_a) if values_a else 0)
            - (sum(values_b) / len(values_b) if values_b else 0),
            "relative_diff": (
                (sum(values_a) / len(values_a) if values_a else 0)
                / (sum(values_b) / len(values_b) if values_b else 1)
                * 100
                - 100
            )
            if values_b and sum(values_b) > 0
            else 0,
        },
    }

    return comparison
