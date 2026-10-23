from observability_client import cloudwatch_client, load_config
from observability_models import normalize_dimensions, normalize_datapoints


def compare_metric_series(metric_name, start_time, end_time, left_dimensions, right_dimensions, period=300):
    cfg = load_config()
    client = cloudwatch_client()
    left = client.get_metric_statistics(
        Namespace=cfg["namespace"],
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=["Average"],
        Dimensions=normalize_dimensions(left_dimensions),
    )
    right = client.get_metric_statistics(
        Namespace=cfg["namespace"],
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=["Average"],
        Dimensions=normalize_dimensions(right_dimensions),
    )
    return {
        "left": normalize_datapoints(left.get("Datapoints", [])),
        "right": normalize_datapoints(right.get("Datapoints", [])),
    }
