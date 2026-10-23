from observability_client import cloudwatch_metric_data
from observability_models import (
    MetricWindowRequest,
    normalize_datapoints,
    normalize_dimensions,
)


def query_metric_window(request: MetricWindowRequest):
    response = cloudwatch_metric_data(
        metric_name=request.metric_name,
        start_time=request.start_time,
        end_time=request.end_time,
        period=int(request.step) if request.step else 60,
        dimensions=normalize_dimensions(request.dimensions),
    )
    results = response.get("MetricDataResults", [])
    if not results:
        return {"metric_name": request.metric_name, "datapoints": []}
    series = results[0]
    datapoints = [
        {"timestamp": ts, "value": val}
        for ts, val in zip(series.get("Timestamps", []), series.get("Values", []))
    ]
    return {
        "metric_name": request.metric_name,
        "datapoints": normalize_datapoints(datapoints),
    }
