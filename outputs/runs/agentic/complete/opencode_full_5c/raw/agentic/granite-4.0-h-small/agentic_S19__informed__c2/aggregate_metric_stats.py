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


def get_aggregated_stats(
    namespace: str,
    metric_name: str,
    statistic: str = "Average",
    dimensions: list[Dict[str, Any]] = None,
    start_time: int = None,
    end_time: int = None,
) -> list[Dict[str, Any]]:
    """Retrieve aggregated statistics for a metric over a time window.
    Returns datapoints with timestamp and the requested statistic.
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
                        "Period": 60,
                        "Stat": statistic,
                        "Unit": "None",
                    },
                    "Label": f"{metric_name} ({statistic})",
                }
            ],
            StartTime=start_time
            or (int((datetime.utcnow() - timedelta(days=1)).timestamp())),
            EndTime=end_time or int(datetime.utcnow().timestamp()),
            ScanBy="TimestampDescending",
        )
        return response["MetricDataResults"][0]["Values"]
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError(f"CloudWatch stats query failed: {exc}")
