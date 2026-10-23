import os
from typing import Dict, Optional

import boto3


def load_observability_config() -> Dict[str, str]:
    return {
        "aws_region": os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")),
        "metric_namespace": os.getenv("AWS_METRIC_NAMESPACE", "Custom/Observability"),
    }


def cloudwatch_client(region_name: Optional[str] = None):
    cfg = load_observability_config()
    return boto3.client("cloudwatch", region_name=region_name or cfg["aws_region"])
