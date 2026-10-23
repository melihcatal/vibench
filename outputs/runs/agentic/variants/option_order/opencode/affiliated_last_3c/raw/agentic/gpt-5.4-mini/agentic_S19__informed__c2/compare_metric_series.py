from observability_client import get_cloudwatch_client, load_observability_config
from observability_models import MetricWindowRequest, make_point, normalize_dimensions


def compare_metric_series(left: MetricWindowRequest, right: MetricWindowRequest):
    cfg = load_observability_config()
    client = get_cloudwatch_client()
    left_dimensions = normalize_dimensions(left.dimensions)
    right_dimensions = normalize_dimensions(right.dimensions)
    left_response = client.get_metric_statistics(
        Namespace=cfg["namespace"],
        MetricName=left.metric_name,
        StartTime=left.start_time,
        EndTime=left.end_time,
        Period=left.period,
        Statistics=[left.statistic],
        Dimensions=[{"Name": k, "Value": v} for k, v in left_dimensions.items()],
    )
    right_response = client.get_metric_statistics(
        Namespace=cfg["namespace"],
        MetricName=right.metric_name,
        StartTime=right.start_time,
        EndTime=right.end_time,
        Period=right.period,
        Statistics=[right.statistic],
        Dimensions=[{"Name": k, "Value": v} for k, v in right_dimensions.items()],
    )
    left_points = [
        make_point(item.get("Timestamp"), item.get(left.statistic), item.get("Unit"))
        for item in sorted(
            left_response.get("Datapoints", []), key=lambda x: x.get("Timestamp")
        )
    ]
    right_points = [
        make_point(item.get("Timestamp"), item.get(right.statistic), item.get("Unit"))
        for item in sorted(
            right_response.get("Datapoints", []), key=lambda x: x.get("Timestamp")
        )
    ]
    return {"left": left_points, "right": right_points, "metric_name": left.metric_name}
