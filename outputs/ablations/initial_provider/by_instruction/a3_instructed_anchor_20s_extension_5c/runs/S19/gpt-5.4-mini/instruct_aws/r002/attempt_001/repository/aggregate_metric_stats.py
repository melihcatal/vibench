from observability_client import cloudwatch_client, load_config
from observability_models import normalize_dimensions, normalize_datapoints


def aggregate_metric_stats(metric_name, start_time, end_time, dimensions=None, period=300):
    cfg = load_config()
    response = cloudwatch_client().get_metric_statistics(
        Namespace=cfg["namespace"],
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=["Average", "Sum", "Minimum", "Maximum", "SampleCount"],
        Dimensions=normalize_dimensions(dimensions),
    )
    return normalize_datapoints(response.get("Datapoints", []))
