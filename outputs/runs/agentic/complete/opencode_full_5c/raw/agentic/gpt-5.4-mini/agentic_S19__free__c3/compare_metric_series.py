from observability_client import cloudwatch_metric_data
from observability_models import MetricComparisonRequest


def _series(metric_name: str, start_time: str, end_time: str, dimensions):
    response = cloudwatch_metric_data(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        dimensions=dimensions,
    )
    results = response.get("MetricDataResults", [])
    if not results:
        return []
    series = results[0]
    return list(series.get("Values", []))


def compare_metric_series(request: MetricComparisonRequest):
    left = _series(
        request.metric_name, request.start_time, request.end_time, request.left_filter
    )
    right = _series(
        request.metric_name, request.start_time, request.end_time, request.right_filter
    )
    left_avg = sum(left) / len(left) if left else None
    right_avg = sum(right) / len(right) if right else None
    return {
        "metric_name": request.metric_name,
        "left_average": left_avg,
        "right_average": right_avg,
    }
