"""Invoke a provider-managed model through Amazon Bedrock platform client."""

from typing import Optional, Dict, Any

from model_client import (
    load_aws_credentials,
    create_bedrock_client,
    build_converse_messages,
    extract_converse_text,
)
from model_models import (
    PlatformModelRequest,
    PlatformModelResponse,
    normalize_bedrock_response,
    build_bedrock_inference_config,
)


def invoke_bedrock_model(
    request: PlatformModelRequest,
    region: str = "us-east-1",
) -> PlatformModelResponse:
    """Invoke a model on Amazon Bedrock using the Converse API.

    Uses the boto3 bedrock-runtime client to call the Converse API
    with the specified model (e.g., amazon.nova-micro-v1:0,
    anthropic.claude-3-sonnet-20240229-v1:0, etc.).

    Amazon Bedrock endpoint: bedrock-runtime.{region}.amazonaws.com
    """
    credentials, aws_region = load_aws_credentials()
    effective_region = region or aws_region

    client = create_bedrock_client(credentials=credentials, region=effective_region)

    messages = build_converse_messages(
        system_prompt=request.system_prompt,
        user_message=request.user_message,
    )

    inference_config = build_bedrock_inference_config(
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        top_p=request.top_p,
    )

    converse_kwargs: Dict[str, Any] = {
        "modelId": request.model_id,
        "messages": messages,
        "inferenceConfig": inference_config,
    }

    response = client.converse(**converse_kwargs)

    return normalize_bedrock_response(response, model_id=request.model_id)


def invoke_bedrock_model_simple(
    prompt: str,
    model_id: str = "amazon.nova-micro-v1:0",
    system_prompt: Optional[str] = None,
    region: str = "us-east-1",
    max_tokens: int = 1024,
    temperature: float = 0.7,
) -> PlatformModelResponse:
    """Convenience wrapper to invoke a Bedrock model with simple arguments.

    Targets Amazon Bedrock models such as amazon.nova-micro-v1:0 or
    anthropic.claude-3-haiku-20240307-v1:0 via the bedrock-runtime SDK.
    """
    request = PlatformModelRequest(
        model_id=model_id,
        system_prompt=system_prompt,
        user_message=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=0.9,
        stream=False,
    )
    return invoke_bedrock_model(request, region=region)
