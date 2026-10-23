from observability_client import cloudwatch_client, normalize_dimensions


def _series(client, namespace, metric_name, start_time, end_time, dimensions, period):
    return client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=["Average"],
        Dimensions=normalize_dimensions(dimensions),
    ).get("Datapoints", [])


def compare_metric_series(
    namespace,
    metric_name,
    start_time,
    end_time,
    left_dimensions=None,
    right_dimensions=None,
    period=300,
):
    client = cloudwatch_client()
    return {
        "left": _series(
            client,
            namespace,
            metric_name,
            start_time,
            end_time,
            left_dimensions,
            period,
        ),
        "right": _series(
            client,
            namespace,
            metric_name,
            start_time,
            end_time,
            right_dimensions,
            period,
        ),
    }
