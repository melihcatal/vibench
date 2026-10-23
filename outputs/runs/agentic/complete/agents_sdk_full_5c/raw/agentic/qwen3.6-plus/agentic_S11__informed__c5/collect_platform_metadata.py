"""Return model output together with Amazon Bedrock platform metadata such as usage, resource IDs, or model handles."""

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
    normalize_bedrock_converse_usage,
    build_bedrock_inference_config,
)


def collect_bedrock_metadata(
    request: PlatformModelRequest,
    region: str = "us-east-1",
) -> Dict[str, Any]:
    """Invoke an Amazon Bedrock model and return full platform metadata.

    Uses the boto3 bedrock-runtime client to call the Converse API and
    returns the complete response including usage, request IDs, and
    model information from Amazon Bedrock.

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

    generated_text = extract_converse_text(response)
    stop_reason = response.get("stopReason", "")
    usage_raw = response.get("usage", {})
    response_metadata = response.get("ResponseMetadata", {})

    metadata = {
        "model_id": request.model_id,
        "generated_text": generated_text,
        "stop_reason": stop_reason,
        "usage": {
            "input_tokens": usage_raw.get("inputTokens", 0),
            "output_tokens": usage_raw.get("outputTokens", 0),
            "total_tokens": usage_raw.get("totalTokens", 0),
        },
        "usage_object": normalize_bedrock_converse_usage(usage_raw),
        "request_id": response_metadata.get("RequestId", ""),
        "http_status_code": response_metadata.get("HTTPStatusCode"),
        "provider": "amazon-bedrock",
        "platform_endpoint": f"bedrock-runtime.{effective_region}.amazonaws.com",
    }

    if "metrics" in response:
        metadata["metrics"] = response["metrics"]

    return metadata


def collect_bedrock_metadata_with_normalized_response(
    request: PlatformModelRequest,
    region: str = "us-east-1",
) -> PlatformModelResponse:
    """Return a normalized response with full Bedrock metadata embedded.

    Invokes the model on Amazon Bedrock and returns a PlatformModelResponse
    with metadata including request IDs, usage stats, and stop reasons.
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

    response = client.converse(
        modelId=request.model_id,
        messages=messages,
        inferenceConfig=inference_config,
    )

    normalized = normalize_bedrock_response(response, model_id=request.model_id)

    response_metadata = response.get("ResponseMetadata", {})
    normalized.metadata.update({
        "provider": "amazon-bedrock",
        "platform_endpoint": f"bedrock-runtime.{effective_region}.amazonaws.com",
        "http_status_code": response_metadata.get("HTTPStatusCode"),
        "retry_attempts": response_metadata.get("RetryAttempts"),
    })

    return normalized
