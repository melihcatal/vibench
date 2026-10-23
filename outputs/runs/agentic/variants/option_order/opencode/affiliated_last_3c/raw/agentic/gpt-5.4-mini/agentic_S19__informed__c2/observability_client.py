import os
from typing import Dict, Optional

import boto3


def load_observability_config() -> Dict[str, str]:
    return {
        "region_name": os.getenv(
            "AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        ),
        "namespace": os.getenv("CLOUDWATCH_NAMESPACE", "AWS/EC2"),
    }


def get_cloudwatch_client(region_name: Optional[str] = None):
    config = load_observability_config()
    return boto3.client("cloudwatch", region_name=region_name or config["region_name"])


def default_metric_dimensions(resource_id: Optional[str] = None) -> Dict[str, str]:
    if resource_id:
        return {"InstanceId": resource_id}
    return {}
