"""
Local configuration and client helper utilities for Managed Model Platform Workflow.

Provides shared configuration loading, Bedrock session setup,
and credential resolution for Amazon Bedrock (boto3) integrations.
"""

import os
from typing import Optional

import boto3
from botocore.config import Config


# Provider-specific identifiers
BEDROCK_REGION: str = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
AWS_ACCESS_KEY_ID: str = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY: str = os.environ.get("AWS_SECRET_ACCESS_KEY", "")

# Common Bedrock client configuration
BEDROCK_CONFIG = Config(
    retries={"max_attempts": 3, "mode": "adaptive"},
    read_timeout=120,
    connect_timeout=30,
)

# Provider-specific model identifiers used across the platform workflow
BEDROCK_MODEL_IDS = {
    "anthropic.claude-3-5-sonnet-20241022-v2:0": "claude-3-5-sonnet-v2",
    "anthropic.claude-3-haiku-20240307-v1:0": "claude-3-haiku",
    "amazon.titan-text-express-v1": "titan-text-express",
    "meta.llama3-70b-instruct-v1:0": "llama3-70b-instruct",
    "mistral.mistral-large-2402-v1:0": "mistral-large",
}


def get_bedrock_runtime_client(
    region_name: Optional[str] = None,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
):
    """Create and return a boto3 Bedrock Runtime client.

    Uses Amazon Bedrock as the concrete provider-managed model platform.
    Provider signals: boto3 import, bedrock-runtime service name, AWS env vars.
    """
    region = region_name or BEDROCK_REGION
    access_key = aws_access_key_id or AWS_ACCESS_KEY_ID
    secret_key = aws_secret_access_key or AWS_SECRET_ACCESS_KEY

    if access_key and secret_key:
        session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )
    else:
        session = boto3.Session(region_name=region)

    return session.client("bedrock-runtime", config=BEDROCK_CONFIG)


def get_bedrock_client(
    region_name: Optional[str] = None,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
):
    """Create and return a boto3 Bedrock management client for model/resource lookups.

    Provider signals: boto3 import, bedrock service name, AWS credentials.
    """
    region = region_name or BEDROCK_REGION
    access_key = aws_access_key_id or AWS_ACCESS_KEY_ID
    secret_key = aws_secret_access_key or AWS_SECRET_ACCESS_KEY

    if access_key and secret_key:
        session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )
    else:
        session = boto3.Session(region_name=region)

    return session.client("bedrock", config=BEDROCK_CONFIG)


def resolve_model_id(model_alias: str) -> str:
    """Resolve a short model alias to a full Amazon Bedrock model ID.

    Provider-specific: maps to Bedrock ARN-style model identifiers.
    """
    for full_id, alias in BEDROCK_MODEL_IDS.items():
        if alias == model_alias or full_id == model_alias:
            return full_id
    # If not found in our map, return as-is (may be a valid Bedrock model ID)
    return model_alias


def build_converse_payload(
    messages: list[dict],
    system_prompt: Optional[str] = None,
    max_tokens: int = 2048,
    temperature: float = 0.7,
    top_p: float = 0.9,
) -> dict:
    """Build a standardized payload for Amazon Bedrock Converse API.

    Provider-specific: conforms to Bedrock Converse API schema.
    """
    payload = {
        "modelId": "",  # Will be filled by caller
        "messages": messages,
        "inferenceConfig": {
            "maxTokens": max_tokens,
            "temperature": temperature,
            "topP": top_p,
        },
    }
    if system_prompt:
        payload["system"] = [{"text": system_prompt}]
    return payload


def load_platform_config() -> dict:
    """Load platform configuration from environment variables.

    Returns a dict with AWS/Bedrock-specific configuration.
    """
    return {
        "provider": "amazon-bedrock",
        "region": BEDROCK_REGION,
        "has_credentials": bool(AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY),
        "available_models": list(BEDROCK_MODEL_IDS.keys()),
    }
