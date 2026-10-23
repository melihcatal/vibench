from observability_client import cloudwatch_metric_data
from observability_models import MetricSummaryRequest


def metric_summary(request: MetricSummaryRequest):
    response = cloudwatch_metric_data(
        metric_name=request.metric_name,
        start_time=request.start_time,
        end_time=request.end_time,
    )
    results = response.get("MetricDataResults", [])
    values = results[0].get("Values", []) if results else []
    if not values:
        return {
            "metric_name": request.metric_name,
            "trend": "unknown",
            "anomaly": False,
        }
    trend = (
        "up" if values[-1] > values[0] else "down" if values[-1] < values[0] else "flat"
    )
    avg = sum(values) / len(values)
    anomaly = values[-1] > avg * 1.5 or values[-1] < avg * 0.5
    return {"metric_name": request.metric_name, "trend": trend, "anomaly": anomaly}
