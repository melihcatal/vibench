from observability_client import cloudwatch_client, load_config


def filter_metric_dimensions(metric_name, start_time, end_time, dimensions, period=300):
    cfg = load_config()
    client = cloudwatch_client()
    resp = client.get_metric_statistics(
        Namespace=cfg.namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=["Average", "Sum"],
        Dimensions=[{"Name": k, "Value": v} for k, v in dimensions.items()],
    )
    return {
        "metric_name": metric_name,
        "dimensions": dimensions,
        "datapoints": resp.get("Datapoints", []),
    }
