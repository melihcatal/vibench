from datetime import timedelta

from observability_client import cloudwatch_client, load_observability_config
from observability_models import MetricWindowRequest, MetricWindowResponse, normalize_datapoints, normalize_dimensions, utcnow, isoformat


def query_metric_window(metric_name: str, minutes: int = 60, namespace: str = None, dimensions=None, statistics=None, period: int = 60) -> MetricWindowResponse:
    cfg = load_observability_config()
    namespace = namespace or cfg["metric_namespace"]
    end_time = utcnow()
    start_time = end_time - timedelta(minutes=minutes)
    request = MetricWindowRequest(namespace=namespace, metric_name=metric_name, start_time=start_time, end_time=end_time, period=period, statistics=statistics or ["Average"], dimensions=dimensions)
    client = cloudwatch_client()
    response = client.get_metric_statistics(
        Namespace=request.namespace,
        MetricName=request.metric_name,
        StartTime=request.start_time,
        EndTime=request.end_time,
        Period=request.period,
        Statistics=request.statistics,
        Dimensions=normalize_dimensions(request.dimensions),
    )
    return MetricWindowResponse(
        namespace=request.namespace,
        metric_name=request.metric_name,
        start_time=isoformat(request.start_time),
        end_time=isoformat(request.end_time),
        period=request.period,
        statistics=list(request.statistics),
        datapoints=normalize_datapoints(response.get("Datapoints", [])),
    )
