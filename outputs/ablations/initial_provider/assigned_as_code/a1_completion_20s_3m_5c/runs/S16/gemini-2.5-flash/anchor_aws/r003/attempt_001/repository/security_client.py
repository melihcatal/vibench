import boto3
from typing import Dict, Any


def get_secrets_manager_client(config: Dict[str, Any] = None):
    config = config or {}
    region_name = config.get("region_name", "us-east-1")  # Default region
    return boto3.client("secretsmanager", region_name=region_name)


def get_translate_client(config: Dict[str, Any] = None):
    config = config or {}
    region_name = config.get("region_name", "us-east-1")
    return boto3.client("translate", region_name=region_name)


def get_comprehend_client(config: Dict[str, Any] = None):
    config = config or {}
    region_name = config.get("region_name", "us-east-1")
    return boto3.client("comprehend", region_name=region_name)


def get_bedrock_runtime_client(config: Dict[str, Any] = None):
    config = config or {}
    region_name = config.get("region_name", "us-east-1")
    return boto3.client("bedrock-runtime", region_name=region_name)
