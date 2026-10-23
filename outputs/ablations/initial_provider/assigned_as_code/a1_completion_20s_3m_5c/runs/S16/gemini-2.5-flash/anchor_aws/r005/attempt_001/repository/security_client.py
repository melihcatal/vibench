import boto3
from typing import Dict, Any


def get_secrets_manager_client(config: Dict[str, Any]) -> Any:
    region_name = config.get("region")
    if not region_name:
        raise ValueError("AWS region must be provided in config.")
    return boto3.client("secretsmanager", region_name=region_name)
