import os
from typing import Optional

import boto3
from botocore.config import Config

from model_models import ModelResource


BEDROCK_RUNTIME_ENDPOINT_TEMPLATE = "bedrock-runtime.{region}.amazonaws.com"
BEDROCK_ENDPOINT_TEMPLATE = "bedrock.{region}.amazonaws.com"

DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
DEFAULT_MODEL_FAMILY = os.environ.get("BEDROCK_MODEL_FAMILY", "anthropic.claude-3")
DEFAULT_MODEL_ID = os.environ.get(
    "BEDROCK_DEFAULT_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0"
)

KNOWN_BEDROCK_RESOURCES: dict[str, ModelResource] = {
    "anthropic.claude-3-sonnet-20240229-v1:0": ModelResource(
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",
        model_arn="arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0",
        provider="anthropic",
        model_family="anthropic.claude-3",
        supported_modalities=["text"],
        max_input_tokens=200000,
        max_output_tokens=4096,
    ),
    "anthropic.claude-3-haiku-20240307-v1:0": ModelResource(
        model_id="anthropic.claude-3-haiku-20240307-v1:0",
        model_arn="arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-haiku-20240307-v1:0",
        provider="anthropic",
        model_family="anthropic.claude-3",
        supported_modalities=["text"],
        max_input_tokens=200000,
        max_output_tokens=4096,
    ),
    "anthropic.claude-3-opus-20240229-v1:0": ModelResource(
        model_id="anthropic.claude-3-opus-20240229-v1:0",
        model_arn="arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-opus-20240229-v1:0",
        provider="anthropic",
        model_family="anthropic.claude-3",
        supported_modalities=["text"],
        max_input_tokens=200000,
        max_output_tokens=4096,
    ),
    "amazon.titan-text-express-v1": ModelResource(
        model_id="amazon.titan-text-express-v1",
        model_arn="arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-text-express-v1",
        provider="amazon",
        model_family="amazon.titan-text",
        supported_modalities=["text"],
        max_input_tokens=8000,
        max_output_tokens=8000,
    ),
    "amazon.titan-embed-text-v1": ModelResource(
        model_id="amazon.titan-embed-text-v1",
        model_arn="arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-embed-text-v1",
        provider="amazon",
        model_family="amazon.titan-embed",
        supported_modalities=["text"],
        max_input_tokens=8000,
        max_output_tokens=0,
    ),
    "amazon.titan-embed-text-v2:0": ModelResource(
        model_id="amazon.titan-embed-text-v2:0",
        model_arn="arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-embed-text-v2:0",
        provider="amazon",
        model_family="amazon.titan-embed",
        supported_modalities=["text"],
        max_input_tokens=8000,
        max_output_tokens=0,
    ),
}


def get_bedrock_runtime_client(
    region: Optional[str] = None,
    endpoint_url: Optional[str] = None,
) -> boto3.client:
    region = region or DEFAULT_REGION
    config = Config(
        retries={"max_attempts": 3, "mode": "standard"},
        read_timeout=60,
        connect_timeout=10,
    )
    session = boto3.Session(
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.environ.get("AWS_SESSION_TOKEN"),
        region_name=region,
    )
    if endpoint_url is None:
        endpoint_url = BEDROCK_RUNTIME_ENDPOINT_TEMPLATE.format(region=region)
    return session.client("bedrock-runtime", endpoint_url=endpoint_url, config=config)


def get_bedrock_client(
    region: Optional[str] = None,
    endpoint_url: Optional[str] = None,
) -> boto3.client:
    region = region or DEFAULT_REGION
    config = Config(
        retries={"max_attempts": 3, "mode": "standard"},
        read_timeout=60,
        connect_timeout=10,
    )
    session = boto3.Session(
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.environ.get("AWS_SESSION_TOKEN"),
        region_name=region,
    )
    if endpoint_url is None:
        endpoint_url = BEDROCK_ENDPOINT_TEMPLATE.format(region=region)
    return session.client("bedrock", endpoint_url=endpoint_url, config=config)


def get_translate_client(
    region: Optional[str] = None,
    endpoint_url: Optional[str] = None,
) -> boto3.client:
    region = region or DEFAULT_REGION
    config = Config(
        retries={"max_attempts": 3, "mode": "standard"},
        read_timeout=30,
        connect_timeout=10,
    )
    session = boto3.Session(
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.environ.get("AWS_SESSION_TOKEN"),
        region_name=region,
    )
    return session.client("translate", endpoint_url=endpoint_url, config=config)


def get_polly_client(
    region: Optional[str] = None,
    endpoint_url: Optional[str] = None,
) -> boto3.client:
    region = region or DEFAULT_REGION
    config = Config(
        retries={"max_attempts": 3, "mode": "standard"},
        read_timeout=60,
        connect_timeout=10,
    )
    session = boto3.Session(
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.environ.get("AWS_SESSION_TOKEN"),
        region_name=region,
    )
    return session.client("polly", endpoint_url=endpoint_url, config=config)


def resolve_model_resource(model_id: Optional[str] = None) -> ModelResource:
    target_id = model_id or DEFAULT_MODEL_ID
    if target_id in KNOWN_BEDROCK_RESOURCES:
        return KNOWN_BEDROCK_RESOURCES[target_id]
    return ModelResource(
        model_id=target_id,
        model_arn=f"arn:aws:bedrock:{DEFAULT_REGION}::foundation-model/{target_id}",
        provider="unknown",
        model_family=target_id.split(".")[0] if "." in target_id else target_id,
        supported_modalities=["text"],
        max_input_tokens=4096,
        max_output_tokens=4096,
    )
