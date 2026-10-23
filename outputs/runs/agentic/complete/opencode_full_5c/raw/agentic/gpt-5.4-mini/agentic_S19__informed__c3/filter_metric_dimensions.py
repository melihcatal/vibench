from observability_client import cloudwatch_client, metric_namespace


def filter_metric_dimensions(
    metric_name, dimensions, start_time, end_time, period=300, stat="Average"
):
    return cloudwatch_client().get_metric_statistics(
        Namespace=metric_namespace(),
        MetricName=metric_name,
        Dimensions=[{"Name": k, "Value": v} for k, v in sorted(dimensions.items())],
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=[stat],
    )
