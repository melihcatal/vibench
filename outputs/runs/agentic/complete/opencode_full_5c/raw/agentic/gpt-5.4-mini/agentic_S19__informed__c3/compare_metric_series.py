from observability_client import cloudwatch_client, metric_namespace


def compare_metric_series(
    metric_name,
    left_dimensions,
    right_dimensions,
    start_time,
    end_time,
    period=300,
    stat="Average",
):
    client = cloudwatch_client()
    common = {
        "Namespace": metric_namespace(),
        "MetricName": metric_name,
        "StartTime": start_time,
        "EndTime": end_time,
        "Period": period,
        "Statistics": [stat],
    }
    left = client.get_metric_statistics(
        **common,
        Dimensions=[
            {"Name": k, "Value": v} for k, v in sorted(left_dimensions.items())
        ],
    )
    right = client.get_metric_statistics(
        **common,
        Dimensions=[
            {"Name": k, "Value": v} for k, v in sorted(right_dimensions.items())
        ],
    )
    return {"left": left, "right": right}
