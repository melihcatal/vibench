"""
Local configuration and client helper utilities for Managed Metrics Monitoring.
Provides AWS CloudWatch client initialization, credential handling, and
common utilities for metrics querying workflows.
"""

import os
import boto3
from botocore.config import Config
from datetime import datetime, timezone
from typing import Optional


# Provider-specific configuration for AWS CloudWatch
CLOUDWATCH_ENDPOINT = "monitoring.amazonaws.com"
DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")


def get_cloudwatch_client(
    region: Optional[str] = None,
    endpoint_url: Optional[str] = None,
    profile: Optional[str] = None,
):
    """
    Initialize and return an AWS CloudWatch client using boto3.

    Args:
        region: AWS region (defaults to AWS_DEFAULT_REGION env var).
        endpoint_url: Optional custom endpoint for CloudWatch API.
        profile: Optional AWS profile name.

    Returns:
        boto3.client configured for CloudWatch monitoring API.
    """
    target_region = region or DEFAULT_REGION
    config = Config(
        retries={"max_attempts": 3, "mode": "adaptive"},
        connect_timeout=10,
        read_timeout=30,
    )

    session_kwargs = {}
    if profile:
        session_kwargs["profile_name"] = profile

    session = boto3.Session(**session_kwargs)

    client_kwargs = {
        "service_name": "cloudwatch",
        "region_name": target_region,
        "config": config,
    }
    if endpoint_url:
        client_kwargs["endpoint_url"] = endpoint_url

    return session.client(**client_kwargs)


def get_cloudwatch_metrics_client(
    region: Optional[str] = None,
    endpoint_url: Optional[str] = None,
    profile: Optional[str] = None,
):
    """
    Initialize and return an AWS CloudWatch client for metrics operations.

    This is an alias for get_cloudwatch_client, kept for semantic clarity
    in code paths that explicitly perform metrics queries.
    """
    return get_cloudwatch_client(region=region, endpoint_url=endpoint_url, profile=profile)


def build_metric_dimensions(dimensions_dict: dict) -> list:
    """
    Convert a dictionary of dimension key-value pairs into the format
    expected by AWS CloudWatch API (list of dicts with 'Name' and 'Value').

    Args:
        dimensions_dict: Dictionary mapping dimension names to values.

    Returns:
        List of dicts suitable for CloudWatch API 'Dimensions' parameter.
    """
    return [
        {"Name": name, "Value": value}
        for name, value in dimensions_dict.items()
    ]


def parse_cloudwatch_timestamp(ts) -> datetime:
    """
    Parse a CloudWatch timestamp string into a timezone-aware datetime.

    Args:
        ts: Timestamp from CloudWatch (datetime object or ISO string).

    Returns:
        Timezone-aware datetime object.
    """
    if isinstance(ts, datetime):
        if ts.tzinfo is None:
            return ts.replace(tzinfo=timezone.utc)
        return ts
    return datetime.fromisoformat(ts).replace(tzinfo=timezone.utc)


def validate_metric_name(name: str) -> bool:
    """
    Validate that a metric name conforms to CloudWatch naming conventions.

    Args:
        name: The metric name to validate.

    Returns:
        True if valid, raises ValueError otherwise.
    """
    if not name or len(name) > 255:
        raise ValueError("Metric name must be between 1 and 255 characters")
    return True


def get_default_time_window(minutes: int = 60):
    """
    Get default start and end times for a metric query window.

    Args:
        minutes: Number of minutes to look back (default 60).

    Returns:
        Tuple of (start_time, end_time) as timezone-aware datetime objects.
    """
    end_time = datetime.now(timezone.utc)
    start_time = end_time.replace(
        minute=end_time.minute - minutes,
        second=0,
        microsecond=0,
    )
    return start_time, end_time
