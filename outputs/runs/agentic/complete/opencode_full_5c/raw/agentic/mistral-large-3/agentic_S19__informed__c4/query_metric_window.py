from typing import Dict, List, Optional, Tuple
import os
from datetime import datetime, timedelta
import boto3
from botocore.exceptions import ClientError


def query_metric_window(
    metric_name: str,
    namespace: str,
    start_time: datetime,
    end_time: datetime,
    dimensions: Optional[List[Dict[str, str]]] = None,
    region: str = "us-east-1",
) -> List[Dict]:
    """
    Query recent datapoints for a named metric over a time window using Amazon CloudWatch Metrics.

    Args:
        metric_name: Name of the CloudWatch metric to query.
        namespace: Namespace of the CloudWatch metric.
        start_time: Start of the time window.
        end_time: End of the time window.
        dimensions: Optional list of dimension dictionaries (e.g., [{"Name": "InstanceId", "Value": "i-12345678"}]).
        region: AWS region where the metric is stored.

    Returns:
        List of datapoints, each represented as a dictionary with "Timestamp", "Value", and "Unit".
    """
    if dimensions is None:
        dimensions = []

    cloudwatch = boto3.client(
        "cloudwatch",
        region_name=region,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    try:
        response = cloudwatch.get_metric_statistics(
            Namespace=namespace,
            MetricName=metric_name,
            Dimensions=dimensions,
            StartTime=start_time,
            EndTime=end_time,
            Period=int((end_time - start_time).total_seconds()),
            Statistics=["SampleCount", "Average", "Sum", "Minimum", "Maximum"],
        )

        datapoints = []
        for point in response["Datapoints"]:
            datapoints.append(
                {
                    "Timestamp": point["Timestamp"],
                    "Value": point["Average"],
                    "Unit": point["Unit"],
                }
            )

        return sorted(datapoints, key=lambda x: x["Timestamp"])
    except ClientError as e:
        raise Exception(f"Failed to query CloudWatch metric: {e}")
