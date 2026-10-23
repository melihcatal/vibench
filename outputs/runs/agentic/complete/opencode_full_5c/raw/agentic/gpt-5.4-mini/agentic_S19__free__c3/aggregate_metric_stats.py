from observability_client import cloudwatch_metric_data
from observability_models import AggregatedMetricRequest, normalize_dimensions


def aggregate_metric_stats(request: AggregatedMetricRequest):
    response = cloudwatch_metric_data(
        metric_name=request.metric_name,
        start_time=request.start_time,
        end_time=request.end_time,
        dimensions=normalize_dimensions(request.dimensions),
    )
    results = response.get("MetricDataResults", [])
    values = results[0].get("Values", []) if results else []
    if not values:
        return {
            "metric_name": request.metric_name,
            "statistic": request.statistic,
            "value": None,
        }
    stat = request.statistic.lower()
    if stat == "sum":
        value = sum(values)
    elif stat == "min":
        value = min(values)
    elif stat == "max":
        value = max(values)
    else:
        value = sum(values) / len(values)
    return {
        "metric_name": request.metric_name,
        "statistic": request.statistic,
        "value": value,
    }
