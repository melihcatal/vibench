from observability_client import cloudwatch_client, load_config


def metric_summary(metric_name, start_time, end_time, period=300):
    cfg = load_config()
    client = cloudwatch_client()
    resp = client.get_metric_statistics(
        Namespace=cfg.namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=["Average", "Maximum", "Minimum"],
    )
    datapoints = sorted(
        resp.get("Datapoints", []), key=lambda item: item.get("Timestamp")
    )
    latest = datapoints[-1] if datapoints else None
    return {
        "metric_name": metric_name,
        "latest": latest,
        "trend": "up"
        if len(datapoints) > 1
        and datapoints[-1].get("Average", 0) >= datapoints[0].get("Average", 0)
        else "flat_or_down",
    }
