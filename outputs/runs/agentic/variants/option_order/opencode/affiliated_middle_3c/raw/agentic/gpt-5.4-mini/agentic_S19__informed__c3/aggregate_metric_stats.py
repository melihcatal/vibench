from observability_client import cloudwatch_client, load_config


def aggregate_metric_stats(metric_name, start_time, end_time, period=300):
    cfg = load_config()
    client = cloudwatch_client()
    resp = client.get_metric_statistics(
        Namespace=cfg.namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=["Average", "Sum", "Minimum", "Maximum", "SampleCount"],
    )
    datapoints = resp.get("Datapoints", [])
    averages = [d.get("Average") for d in datapoints if d.get("Average") is not None]
    return {
        "metric_name": metric_name,
        "count": len(datapoints),
        "average": sum(averages) / len(averages) if averages else None,
        "minimum": min(
            (d.get("Minimum") for d in datapoints if d.get("Minimum") is not None),
            default=None,
        ),
        "maximum": max(
            (d.get("Maximum") for d in datapoints if d.get("Maximum") is not None),
            default=None,
        ),
        "sum": sum((d.get("Sum") or 0) for d in datapoints),
    }
