import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3


@dataclass
class PlatformConfig:
    region_name: str
    model_id: str
    inference_profile_arn: Optional[str] = None
    endpoint_name: Optional[str] = None
    guardrail_identifier: Optional[str] = None


def load_platform_config() -> PlatformConfig:
    return PlatformConfig(
        region_name=os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1")),
        model_id=os.environ.get("AWS_BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0"),
        inference_profile_arn=os.environ.get("AWS_BEDROCK_INFERENCE_PROFILE_ARN"),
        endpoint_name=os.environ.get("AWS_SAGEMAKER_ENDPOINT_NAME"),
        guardrail_identifier=os.environ.get("AWS_BEDROCK_GUARDRAIL_IDENTIFIER"),
    )


def bedrock_runtime_client(region_name: Optional[str] = None):
    config = load_platform_config()
    return boto3.client("bedrock-runtime", region_name=region_name or config.region_name)


def bedrock_client(region_name: Optional[str] = None):
    config = load_platform_config()
    return boto3.client("bedrock", region_name=region_name or config.region_name)


def sagemaker_runtime_client(region_name: Optional[str] = None):
    config = load_platform_config()
    return boto3.client("sagemaker-runtime", region_name=region_name or config.region_name)


def invoke_bedrock_model(payload: Dict[str, Any], model_id: Optional[str] = None, region_name: Optional[str] = None) -> Dict[str, Any]:
    client = bedrock_runtime_client(region_name)
    config = load_platform_config()
    response = client.converse(
        modelId=model_id or config.model_id,
        messages=payload.get("messages", []),
        inferenceConfig=payload.get("inferenceConfig", {}),
        system=payload.get("system", []),
        toolConfig=payload.get("toolConfig"),
        guardrailConfig={"guardrailIdentifier": config.guardrail_identifier} if config.guardrail_identifier else None,
    )
    return response
