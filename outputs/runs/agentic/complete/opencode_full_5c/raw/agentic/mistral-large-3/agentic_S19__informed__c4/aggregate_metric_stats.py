from typing import Dict, List, Optional
import os
from datetime import datetime
import boto3
from botocore.exceptions import ClientError


def aggregate_metric_stats(
    metric_name: str,
    namespace: str,
    start_time: datetime,
    end_time: datetime,
    dimensions: Optional[List[Dict[str, str]]] = None,
    region: str = "us-east-1",
) -> Dict:
    """
    Retrieve aggregated statistics for a metric over a time window using Amazon CloudWatch Metrics.

    Args:
        metric_name: Name of the CloudWatch metric to query.
        namespace: Namespace of the CloudWatch metric.
        start_time: Start of the time window.
        end_time: End of the time window.
        dimensions: Optional list of dimension dictionaries (e.g., [{"Name": "InstanceId", "Value": "i-12345678"}]).
        region: AWS region where the metric is stored.

    Returns:
        Dictionary containing aggregated statistics (e.g., "Average", "Sum", "Minimum", "Maximum", "SampleCount").
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
            Statistics=["Average", "Sum", "Minimum", "Maximum", "SampleCount"],
        )

        if not response["Datapoints"]:
            return {
                "Average": None,
                "Sum": None,
                "Minimum": None,
                "Maximum": None,
                "SampleCount": 0,
            }

        latest_datapoint = max(response["Datapoints"], key=lambda x: x["Timestamp"])
        return {
            "Average": latest_datapoint.get("Average"),
            "Sum": latest_datapoint.get("Sum"),
            "Minimum": latest_datapoint.get("Minimum"),
            "Maximum": latest_datapoint.get("Maximum"),
            "SampleCount": latest_datapoint.get("SampleCount"),
        }
    except ClientError as e:
        raise Exception(f"Failed to retrieve CloudWatch metric statistics: {e}")
