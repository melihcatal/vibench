from observability_client import cloudwatch_metric_data
from observability_models import MetricWindowRequest, normalize_dimensions


def filter_metric_dimensions(request: MetricWindowRequest):
    response = cloudwatch_metric_data(
        metric_name=request.metric_name,
        start_time=request.start_time,
        end_time=request.end_time,
        dimensions=normalize_dimensions(request.dimensions),
    )
    results = response.get("MetricDataResults", [])
    if not results:
        return {"metric_name": request.metric_name, "filtered_datapoints": []}
    series = results[0]
    return {
        "metric_name": request.metric_name,
        "filtered_datapoints": [
            {"timestamp": ts, "value": val}
            for ts, val in zip(series.get("Timestamps", []), series.get("Values", []))
        ],
    }
