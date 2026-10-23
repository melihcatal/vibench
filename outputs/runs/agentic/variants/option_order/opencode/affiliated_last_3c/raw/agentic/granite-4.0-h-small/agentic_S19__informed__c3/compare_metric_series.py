import boto3
from observability_client import get_aws_credentials, normalize_response


def compare_metric_series(
    metric_name, start_time, end_time, resource1, resource2, period=60
):
    """Compare metric values for two resources or dimension filters over the same window using Amazon CloudWatch Metrics.

    Parameters:
        metric_name (str): The name of the metric.
        start_time (int): Unix timestamp (seconds) for the start of the window.
        end_time (int): Unix timestamp (seconds) for the end of the window.
        resource1 (dict): First dimension filter, e.g., {'Name': 'InstanceId', 'Value': 'i-12345'}.
        resource2 (dict): Second dimension filter, e.g., {'Name': 'InstanceId', 'Value': 'i-67890'}.
        period (int, optional): Granularity of returned data points in seconds (default 60).

    Returns:
        dict: Comparison result with normalized values for each resource.
    """
    client = boto3.client(
        "cloudwatch",
        aws_access_key_id=get_aws_credentials().get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=get_aws_credentials().get("AWS_SECRET_ACCESS_KEY"),
        region_name="us-east-1",
    )

    # Query first resource
    response1 = client.get_metric_data(
        MetricDataQueries=[
            {
                "Id": "m1",
                "MetricStat": {
                    "Metric": {
                        "Namespace": "AWS/EC2",
                        "MetricName": metric_name,
                        "Dimensions": [resource1],
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

    # Query second resource
    response2 = client.get_metric_data(
        MetricDataQueries=[
            {
                "Id": "m2",
                "MetricStat": {
                    "Metric": {
                        "Namespace": "AWS/EC2",
                        "MetricName": metric_name,
                        "Dimensions": [resource2],
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

    # Normalize responses
    norm1 = normalize_response(response1, metric_name)
    norm2 = normalize_response(response2, metric_name)
    return {"resource1": norm1, "resource2": norm2}
