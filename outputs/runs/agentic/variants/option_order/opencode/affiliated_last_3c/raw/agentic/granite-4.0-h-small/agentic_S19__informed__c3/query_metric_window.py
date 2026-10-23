import boto3
from observability_client import get_aws_credentials, normalize_response


def query_metric_window(metric_name, start_time, end_time, period=60):
    """Query recent datapoints for a named metric over a time window using Amazon CloudWatch Metrics.

    Parameters:
        metric_name (str): The name of the metric.
        start_time (int): Unix timestamp (seconds) for the start of the window.
        end_time (int): Unix timestamp (seconds) for the end of the window.
        period (int, optional): Granularity of returned data points in seconds (default 60).

    Returns:
        list: Normalized datapoints with standardized fields.
    """
    client = boto3.client(
        "cloudwatch",
        aws_access_key_id=get_aws_credentials().get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=get_aws_credentials().get("AWS_SECRET_ACCESS_KEY"),
        region_name="us-east-1",  # default region can be configured elsewhere
    )

    response = client.get_metric_data(
        MetricDataQueries=[
            {
                "Id": "m1",
                "MetricStat": {
                    "Metric": {
                        "Namespace": "AWS/EC2",  # placeholder namespace, can be dynamic
                        "MetricName": metric_name,
                        "Dimensions": [],  # optional dimensions can be added here
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
        MaxDatapoints=500,  # limit for simplicity
    )

    # Normalize and filter the response
    return normalize_response(response, metric_name)
