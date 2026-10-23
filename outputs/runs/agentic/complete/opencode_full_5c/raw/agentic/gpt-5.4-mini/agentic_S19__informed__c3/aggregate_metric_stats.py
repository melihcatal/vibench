from observability_client import cloudwatch_client, metric_namespace
from observability_models import MetricWindowRequest, normalize_dimensions


def aggregate_metric_stats(request: MetricWindowRequest):
    client = cloudwatch_client()
    return client.get_metric_statistics(
        Namespace=metric_namespace(),
        MetricName=request.metric_name,
        Dimensions=normalize_dimensions(request.dimensions),
        StartTime=request.start_time,
        EndTime=request.end_time,
        Period=request.period,
        Statistics=["Average", "Sum", "Minimum", "Maximum", "SampleCount"],
    )
