"""
Local configuration and client helper utilities for Managed Metrics Monitoring.

Uses AWS CloudWatch as the concrete metrics provider.
Provider signals:
  - boto3 client creation for 'monitoring' (CloudWatch API)
  - CloudWatch endpoint URL patterns
  - AWS environment variables
"""

import os
import boto3
from botocore.config import Config

CLOUDWATCH_ENDPOINT = os.getenv("CLOUDWATCH_ENDPOINT", "https://monitoring.us-east-1.amazonaws.com")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")


def create_cloudwatch_client():
    """Create a boto3 CloudWatch client with configuration from environment."""
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    )
    config = Config(
        retries={"max_attempts": 3, "mode": "standard"},
        user_agent_extra="observability-metrics-monitor/1.0",
    )
    client = session.client("monitoring", endpoint_url=CLOUDWATCH_ENDPOINT, config=config)
    return client


def build_metric_query(metric_name, namespace, period=60):
    """Build a standardized CloudWatch metric query payload."""
    return {
        "Namespace": namespace,
        "MetricName": metric_name,
        "Period": period,
    }


def build_dimension_filters(dimensions):
    """Build dimension filter list for CloudWatch API."""
    if not dimensions:
        return []
    return [{"Name": k, "Value": v} for k, v in dimensions.items()]


def normalize_cloudwatch_response(raw_response):
    """Normalize CloudWatch GetMetricData response into a uniform format."""
    results = []
    for metric_result in raw_response.get("MetricDataResults", []):
        result = {
            "metric_id": metric_result.get("Id"),
            "label": metric_result.get("Label"),
            "timestamps": metric_result.get("Timestamps", []),
            "values": metric_result.get("Values", []),
            "status_code": metric_result.get("StatusCode"),
        }
        results.append(result)
    return results


def get_account_id_from_client(client):
    """Retrieve the AWS account ID associated with the CloudWatch client."""
    sts = boto3.client("sts")
    identity = sts.get_caller_identity()
    return identity.get("Account")
