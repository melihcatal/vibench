from observability_client import get_cloudwatch_client, load_observability_config
from observability_models import (
    MetricWindowRequest,
    MetricStatsResponse,
    make_stats,
    normalize_dimensions,
)


def aggregate_metric_stats(request: MetricWindowRequest) -> MetricStatsResponse:
    cfg = load_observability_config()
    client = get_cloudwatch_client()
    dimensions = normalize_dimensions(request.dimensions)
    response = client.get_metric_statistics(
        Namespace=cfg["namespace"],
        MetricName=request.metric_name,
        StartTime=request.start_time,
        EndTime=request.end_time,
        Period=request.period,
        Statistics=["Minimum", "Maximum", "Average", "Sum", "SampleCount"],
        Dimensions=[{"Name": k, "Value": v} for k, v in dimensions.items()],
    )
    datapoints = response.get("Datapoints", [])
    if datapoints:
        latest = sorted(datapoints, key=lambda x: x.get("Timestamp"))[-1]
        payload = {
            "minimum": latest.get("Minimum"),
            "maximum": latest.get("Maximum"),
            "average": latest.get("Average"),
            "sum": latest.get("Sum"),
            "sample_count": latest.get("SampleCount"),
        }
    else:
        payload = {}
    return make_stats(request.metric_name, "Aggregate", payload)
