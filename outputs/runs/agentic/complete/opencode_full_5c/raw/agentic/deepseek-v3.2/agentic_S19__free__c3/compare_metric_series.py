import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2


def compare_metric_series(metric_name, filter_a, filter_b, window_minutes=60):
    """Compare metric values for two resources or dimension filters over the same window."""
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

    aggregation = monitoring_v3.Aggregation()
    aggregation.alignment_period = {"seconds": 300}
    aggregation.per_series_aligner = monitoring_v3.Aggregation.Aligner.ALIGN_MEAN
    aggregation.cross_series_reducer = monitoring_v3.Aggregation.Reducer.REDUCE_MEAN

    try:
        results_a = client.list_time_series(
            request={
                "name": project_name,
                "filter": filter_a_str,
                "interval": interval,
                "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
                "aggregation": aggregation,
            }
        )

        results_b = client.list_time_series(
            request={
                "name": project_name,
                "filter": filter_b_str,
                "interval": interval,
                "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
                "aggregation": aggregation,
            }
        )

        def extract_values(series_list):
            values = []
            for series in series_list:
                for point in series.points:
                    value = (
                        point.value.double_value
                        if point.value.double_value
                        else point.value.int64_value
                    )
                    if value is not None:
                        values.append(value)
            return values

        values_a = extract_values(results_a)
        values_b = extract_values(results_b)

        comparison = {
            "metric": metric_name,
            "window_minutes": window_minutes,
            "filter_a": filter_a,
            "filter_b": filter_b,
            "count_a": len(values_a),
            "count_b": len(values_b),
            "avg_a": sum(values_a) / len(values_a) if values_a else None,
            "avg_b": sum(values_b) / len(values_b) if values_b else None,
            "min_a": min(values_a) if values_a else None,
            "min_b": min(values_b) if values_b else None,
            "max_a": max(values_a) if values_a else None,
            "max_b": max(values_b) if values_b else None,
        }

        if values_a and values_b:
            avg_a = sum(values_a) / len(values_a)
            avg_b = sum(values_b) / len(values_b)
            comparison["difference"] = avg_a - avg_b
            comparison["percent_difference"] = (
                ((avg_a - avg_b) / avg_b * 100) if avg_b != 0 else None
            )

        return comparison

    except Exception as e:
        print(f"Error comparing metric series: {e}")
        return {
            "metric": metric_name,
            "window_minutes": window_minutes,
            "filter_a": filter_a,
            "filter_b": filter_b,
            "error": str(e),
        }
