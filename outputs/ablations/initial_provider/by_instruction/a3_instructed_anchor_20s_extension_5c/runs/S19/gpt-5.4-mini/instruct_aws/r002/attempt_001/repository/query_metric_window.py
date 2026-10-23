from observability_client import cloudwatch_client, load_config, time_window_minutes, to_utc
from observability_models import MetricWindowRequest, MetricSeriesResponse, normalize_datapoints, normalize_dimensions


def query_metric_window(metric_name, minutes=60, dimensions=None, period=300, statistics=None):
    cfg = load_config()
    start_time, end_time = time_window_minutes(minutes)
    request = MetricWindowRequest(
        namespace=cfg["namespace"],
        metric_name=metric_name,
        start_time=to_utc(start_time),
        end_time=to_utc(end_time),
        dimensions=dimensions or {},
        period=period,
        statistics=statistics or ["Average"],
    )
    response = cloudwatch_client().get_metric_statistics(
        Namespace=request.namespace,
        MetricName=request.metric_name,
        StartTime=request.start_time,
        EndTime=request.end_time,
        Period=request.period,
        Statistics=request.statistics,
        Dimensions=normalize_dimensions(request.dimensions),
    )
    return MetricSeriesResponse(
        metric_name=request.metric_name,
        namespace=request.namespace,
        datapoints=normalize_datapoints(response.get("Datapoints", [])),
    )
