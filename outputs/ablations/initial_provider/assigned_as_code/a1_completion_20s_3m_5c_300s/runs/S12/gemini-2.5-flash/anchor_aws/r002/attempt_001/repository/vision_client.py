import boto3
from typing import Dict, Any

def get_rekognition_client(config: Dict[str, Any]) -> Any:
    """Initializes and returns an AWS Rekognition client."""
    region_name = config.get("region")
    if not region_name:
        raise ValueError("AWS region must be provided in config.")
    return boto3.client("rekognition", region_name=region_name)

def get_bedrock_runtime_client(config: Dict[str, Any]) -> Any:
    """Initializes and returns an AWS Bedrock Runtime client."""
    region_name = config.get("region")
    if not region_name:
        raise ValueError("AWS region for Bedrock must be provided in config.")
    return boto3.client("bedrock-runtime", region_name=region_name)

def get_translate_client(config: Dict[str, Any]) -> Any:
    """Initializes and returns an AWS Translate client."""
    region_name = config.get("region")
    if not region_name:
        raise ValueError("AWS region for Translate must be provided in config.")
    return boto3.client("translate", region_name=region_name)

def get_comprehend_client(config: Dict[str, Any]) -> Any:
    """Initializes and returns an AWS Comprehend client."""
    region_name = config.get("region")
    if not region_name:
        raise ValueError("AWS region for Comprehend must be provided in config.")
    return boto3.client("comprehend", region_name=region_name)

def get_s3_client(config: Dict[str, Any]) -> Any:
    """Initializes and returns an AWS S3 client."""
    region_name = config.get("region")
    if not region_name:
        raise ValueError("AWS region for S3 must be provided in config.")
    return boto3.client("s3", region_name=region_name)
