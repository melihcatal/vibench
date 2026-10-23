from observability_client import cloudwatch_client, normalize_dimensions


def filter_metric_dimensions(
    namespace, metric_name, start_time, end_time, dimensions=None, period=300
):
    client = cloudwatch_client()
    response = client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=["Average"],
        Dimensions=normalize_dimensions(dimensions),
    )
    return response.get("Datapoints", [])
