from observability_client import cloudwatch_client, load_config
from observability_models import (
    MetricWindowRequest,
    MetricQueryResponse,
    normalize_datapoints,
)


def query_metric_window(metric_name, start_time, end_time, period=300):
    cfg = load_config()
    client = cloudwatch_client()
    request = MetricWindowRequest(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        period=period,
        namespace=cfg.namespace,
    )
    response = client.get_metric_statistics(
        Namespace=request.namespace,
        MetricName=request.metric_name,
        StartTime=request.start_time,
        EndTime=request.end_time,
        Period=request.period,
        Statistics=["Average", "Sum", "Minimum", "Maximum"],
    )
    points = normalize_datapoints(response.get("Datapoints", []))
    return MetricQueryResponse(
        label=metric_name,
        timestamps=[p["timestamp"] for p in points],
        values=[p["value"] for p in points],
        status_code="ok",
    )
