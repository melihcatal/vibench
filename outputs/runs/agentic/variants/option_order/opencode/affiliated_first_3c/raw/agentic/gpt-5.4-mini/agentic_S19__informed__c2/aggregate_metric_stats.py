from observability_client import cloudwatch_client, normalize_dimensions


def aggregate_metric_stats(
    namespace, metric_name, start_time, end_time, period=300, dimensions=None
):
    client = cloudwatch_client()
    response = client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=["Average", "Sum", "Minimum", "Maximum", "SampleCount"],
        Dimensions=normalize_dimensions(dimensions),
    )
    datapoints = response.get("Datapoints", [])
    return {
        "count": len(datapoints),
        "average": [d.get("Average") for d in datapoints],
        "sum": [d.get("Sum") for d in datapoints],
        "minimum": [d.get("Minimum") for d in datapoints],
        "maximum": [d.get("Maximum") for d in datapoints],
    }
