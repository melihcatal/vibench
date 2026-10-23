import boto3
from typing import Dict, Any

def get_translate_client(region_name: str = None):
    """
    Returns a boto3 Translate client.
    """
    return boto3.client("translate", region_name=region_name)

def get_comprehend_client(region_name: str = None):
    """
    Returns a boto3 Comprehend client.
    """
    return boto3.client("comprehend", region_name=region_name)

def get_bedrock_runtime_client(region_name: str = None):
    """
    Returns a boto3 Bedrock Runtime client.
    """
    return boto3.client("bedrock-runtime", region_name=region_name)

def get_polly_client(region_name: str = None):
    """
    Returns a boto3 Polly client.
    """
    return boto3.client("polly", region_name=region_name)


def get_config(config: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Provides a default configuration and merges with any provided config.
    """
    default_config = {
        "region": "us-east-1",  # Default AWS region
    }
    return {**default_config, **(config or {})}
