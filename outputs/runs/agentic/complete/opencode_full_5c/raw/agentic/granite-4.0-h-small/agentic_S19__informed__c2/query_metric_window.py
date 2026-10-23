import os
from typing import Any, Dict

import boto3
from botocore.exceptions import BotoCoreError, ClientError

# Use AWS credentials from environment (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)


def create_cloudwatch_client() -> boto3.client:
    """Create and cache a CloudWatch client."""
    if not (
        (aws_access := os.getenv("AWS_ACCESS_KEY_ID"))
        and (aws_secret := os.getenv("AWS_SECRET_ACCESS_KEY"))
    ):
        raise RuntimeError("Missing AWS credentials")
    return boto3.client(
        "cloudwatch",
        aws_access_key_id=aws_access,
        aws_secret_access_key=aws_secret,
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )


cw_client = create_cloudwatch_client()


def get_metric_data(
    namespace: str,
    metric_name: str,
    dimensions: list[Dict[str, Any]],
    start_time: int,
    end_time: int,
    period: int = 60,
) -> list[Dict[str, Any]]:
    """Query recent datapoints for a named metric over a time window.
    Returns a list of datapoint dicts (Timestamp, Value, etc.)
    """
    try:
        response = cw_client.get_metric_data(
            MetricDataQueries=[
                {
                    "Id": "m1",
                    "MetricStat": {
                        "Metric": {
                            "Namespace": namespace,
                            "MetricName": metric_name,
                        },
                        "Period": period,
                        "Stat": "Average",  # change to 'Sum', 'Maximum', etc. as needed
                        "Unit": "None",
                    },
                    "Label": f"{metric_name} (avg)",
                }
            ],
            StartTime=start_time,
            EndTime=end_time,
            ScanBy="TimestampDescending",
        )
        return response["MetricDataResults"][0]["Values"]
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError(f"CloudWatch query failed: {exc}")
