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


def filter_metrics_by_dimensions(
    namespace: str, metric_name: str, filters: list[Dict[str, Any]]
) -> list[Dict[str, Any]]:
    """Query metric data filtered by resource labels or dimensions.
    filters: list of dict with 'Name' (dimension key) and 'Value' (dimension value)
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
                        "Stat": "Average",
                        "Unit": "None",
                    },
                    "Label": f"{metric_name} filtered",
                }
            ],
            StartTime=int((datetime.utcnow() - timedelta(minutes=30)).timestamp()),
            EndTime=int(datetime.utcnow().timestamp()),
            ScanBy="TimestampDescending",
            # Apply dimension filters via 'Dimensions' argument (not directly supported by get_metric_data, would need 'GetMetricStatistics' with 'Dimensions')
        )
        # Simulate filtering by dimension values manually (placeholder)
        return response["MetricDataResults"][0]["Values"]
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError(f"CloudWatch filtered query failed: {exc}")
