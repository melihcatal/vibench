# [HELPER] observability_client.py

# Local helper to create a configured client for Managed Metrics Monitoring.
# Provider: Amazon CloudWatch Metrics (boto3 SDK)
# Credentials are loaded from AWS environment variables for safety.

import os
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


def get_cloudwatch_client():
    """Create and return a CloudWatch client with proper credential handling.

    Uses AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_REGION (optional).
    Throws RuntimeError if credentials are missing.
    """
    try:
        # Attempt to create the client; boto3 will automatically pick up env vars.
        client = boto3.client("cloudwatch")
        # Simple sanity check to ensure credentials work.
        client.get_metric_statistics(
            Namespace="AWS/EC2",
            MetricName="CPUUtilization",
            Dimensions=[],
            StartTime=datetime.utcnow() - timedelta(minutes=5),
            EndTime=datetime.utcnow(),
            Period=300,
            Statistics=["Average"],
        )
        return client
    except (NoCredentialsError, PartialCredentialsError) as exc:
        raise RuntimeError("Missing or invalid AWS credentials") from exc
    except Exception as exc:
        raise RuntimeError("Failed to create CloudWatch client") from exc
