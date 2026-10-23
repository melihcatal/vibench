import boto3
from observability_client import get_aws_credentials, normalize_response


def filter_metric_dimensions(
    metric_name, start_time, end_time, dimensions=None, period=60
):
    """Query metric data filtered by resource labels or dimensions using Amazon CloudWatch Metrics.

    Parameters:
        metric_name (str): The name of the metric.
        start_time (int): Unix timestamp (seconds) for the start of the window.
        end_time (int): Unix timestamp (seconds) for the end of the window.
        dimensions (list[dict], optional): List of dimension filters, e.g., [{'Name': 'InstanceId', 'Value': 'i-12345'}].
        period (int, optional): Granularity of returned data points in seconds (default 60).

    Returns:
        list: Normalized filtered datapoints with standardized fields.
    """
    client = boto3.client(
        "cloudwatch",
        aws_access_key_id=get_aws_credentials().get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=get_aws_credentials().get("AWS_SECRET_ACCESS_KEY"),
        region_name="us-east-1",
    )

    response = client.get_metric_data(
        MetricDataQueries=[
            {
                "Id": "m1",
                "MetricStat": {
                    "Metric": {
                        "Namespace": "AWS/EC2",  # placeholder namespace
                        "MetricName": metric_name,
                        "Dimensions": dimensions if dimensions else [],
                    },
                    "Period": period,
                    "Stat": "Average",
                    "Unit": "None",
                },
                "ReturnData": True,
            }
        ],
        StartTime=start_time,
        EndTime=end_time,
        ScanBy="TimestampDescending",
        MaxDatapoints=500,
    )
    return normalize_response(response, metric_name)
