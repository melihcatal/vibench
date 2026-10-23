import boto3
from observability_client import get_aws_credentials, normalize_response


def aggregate_metric_stats(metric_name, start_time, end_time, statistic="Average"):
    """Retrieve aggregated statistics for a metric over a time window using Amazon CloudWatch Metrics.

    Parameters:
        metric_name (str): The name of the metric.
        start_time (int): Unix timestamp (seconds) for the start of the window.
        end_time (int): Unix timestamp (seconds) for the end of the window.
        statistic (str, optional): Statistic to compute (default 'Average').

    Returns:
        list: Normalized aggregated datapoints with standardized fields.
    """
    client = boto3.client(
        "cloudwatch",
        aws_access_key_id=get_aws_credentials().get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=get_aws_credentials().get("AWS_SECRET_ACCESS_KEY"),
        region_name="us-east-1",
    )

    response = client.get_metric_statistics(
        Namespace="AWS/EC2",  # placeholder namespace
        MetricName=metric_name,
        Dimensions=[],  # optional dimensions can be added here
        StartTime=start_time,
        EndTime=end_time,
        Period=60,  # default period, adjust as needed
        Statistics=[statistic],
    )
    return normalize_response(response, metric_name)
