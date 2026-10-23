import os
from typing import Any

# Managed Metrics Monitoring client helper utilities

# Example: environment variable based credential loading
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# Example: simple client wrapper for CloudWatch via Boto3
# In real code this would be parameterized; here we expose a helper that matches the same-scenario implementation


def get_metric_data(
    namespace: str,
    metric_name: str,
    dimensions: list[Dict[str, Any]] = None,
    start_time: int = None,
    end_time: int = None,
) -> Any:
    """Convenience wrapper around the same CloudWatch query used in query_metric_window.py"""
    import boto3
    from botocore.exceptions import BotoCoreError, ClientError

    if not (AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY):
        raise RuntimeError("Missing AWS credentials")
    client = boto3.client(
        "cloudwatch",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    )
    if start_time is None:
        start_time = int(
            (datetime.utcnow() - datetime.timedelta(minutes=30)).timestamp()
        )
    if end_time is None:
        end_time = int(datetime.utcnow().timestamp())
    try:
        response = client.get_metric_data(
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
                    "Label": f"{metric_name} (avg)",
                }
            ],
            StartTime=start_time,
            EndTime=end_time,
            ScanBy="TimestampDescending",
        )
        return response["MetricDataResults"][0]["Values"]
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError(f"Client helper query failed: {exc}")
