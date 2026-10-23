import os
import boto3


def aws_region():
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def bedrock_runtime_client():
    return boto3.client("bedrock-runtime", region_name=aws_region())


def bedrock_agent_runtime_client():
    return boto3.client("bedrock-agent-runtime", region_name=aws_region())


def bedrock_client():
    return boto3.client("bedrock", region_name=aws_region())


def default_model_id():
    return os.getenv("BEDROCK_MODEL_ID") or "anthropic.claude-3-sonnet-20240229-v1:0"
