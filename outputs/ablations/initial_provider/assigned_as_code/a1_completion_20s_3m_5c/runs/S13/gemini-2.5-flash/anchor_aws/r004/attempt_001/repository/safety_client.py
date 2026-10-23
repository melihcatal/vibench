import boto3
from typing import Dict, Any

def get_aws_client(service_name: str, config: Dict[str, Any] = None):
    config = config or {}
    region_name = config.get("region", "us-east-1")
    return boto3.client(service_name, region_name=region_name)
