from observability_client import cloudwatch_client, load_config


def compare_metric_series(
    metric_name, start_time, end_time, left_dimensions, right_dimensions, period=300
):
    cfg = load_config()
    client = cloudwatch_client()
    common = dict(
        Namespace=cfg.namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=["Average"],
    )
    left = client.get_metric_statistics(
        **common,
        Dimensions=[{"Name": k, "Value": v} for k, v in left_dimensions.items()],
    ).get("Datapoints", [])
    right = client.get_metric_statistics(
        **common,
        Dimensions=[{"Name": k, "Value": v} for k, v in right_dimensions.items()],
    ).get("Datapoints", [])
    return {"metric_name": metric_name, "left": left, "right": right}
