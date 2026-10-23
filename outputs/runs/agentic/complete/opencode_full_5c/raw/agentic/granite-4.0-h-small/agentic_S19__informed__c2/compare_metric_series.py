import os
import datetime
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


def compare_two_metric_series(
    namespace1: str,
    metric_name1: str,
    namespace2: str,
    metric_name2: str,
    dimensions: list[Dict[str, Any]] = None,
    start_time: int = None,
    end_time: int = None,
) -> tuple[list[Dict[str, Any]], list[Dict[str, Any]]]:
    """Compare metric values for two resources or dimension filters over the same window.
    Returns tuple of (resource1 datapoints, resource2 datapoints)
    """
    try:
        response1 = cw_client.get_metric_data(
            MetricDataQueries=[
                {
                    "Id": "m1",
                    "MetricStat": {
                        "Metric": {
                            "Namespace": namespace1,
                            "MetricName": metric_name1,
                        },
                        "Period": 60,
                        "Stat": "Average",
                        "Unit": "None",
                    },
                    "Label": f"{metric_name1} (avg)",
                }
            ],
            StartTime=start_time
            or int(
                (
                    datetime.datetime.utcnow() - datetime.timedelta(minutes=30)
                ).timestamp()
            ),
            EndTime=end_time or int(datetime.datetime.utcnow().timestamp()),
            ScanBy="TimestampDescending",
        )
        response2 = cw_client.get_metric_data(
            MetricDataQueries=[
                {
                    "Id": "m2",
                    "MetricStat": {
                        "Metric": {
                            "Namespace": namespace2,
                            "MetricName": metric_name2,
                        },
                        "Period": 60,
                        "Stat": "Average",
                        "Unit": "None",
                    },
                    "Label": f"{metric_name2} (avg)",
                }
            ],
            StartTime=start_time
            or int(
                (
                    datetime.datetime.utcnow() - datetime.timedelta(minutes=30)
                ).timestamp()
            ),
            EndTime=end_time or int(datetime.datetime.utcnow().timestamp()),
            ScanBy="TimestampDescending",
        )
        return response1["MetricDataResults"][0]["Values"], response2[
            "MetricDataResults"
        ][0]["Values"]
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError(f"CloudWatch comparison query failed: {exc}")
