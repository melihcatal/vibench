import os
import boto3


def get_aws_credentials() -> dict:
    """Load AWS credentials from environment variables or shared config file.

    Returns:
        dict: Dictionary containing AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.
    """
    return {
        "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
        "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY"),
    }


def normalize_response(response, metric_name: str) -> list:
    """Normalize CloudWatch response into a consistent structure.

    Args:
        response (dict): Raw CloudWatch API response.
        metric_name (str): Name of the queried metric.

    Returns:
        list: List of normalized datapoints with keys: Timestamp, Value, and MetricName.
    """
    datapoints = response.get("MetricDataResults", [{}])[0].get("Datapoints", [])
    normalized = []
    for dp in datapoints:
        normalized.append(
            {
                "Timestamp": dp.get("Timestamp"),
                "Value": dp.get("Average"),  # use appropriate field if Stat differs
                "MetricName": metric_name,
            }
        )
    return normalized
