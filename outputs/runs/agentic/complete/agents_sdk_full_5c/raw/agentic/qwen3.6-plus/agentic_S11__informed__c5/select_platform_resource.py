"""Resolve a provider-specific model, deployment, or inference resource before invocation."""

import os
from typing import Optional, List, Dict, Any

from model_client import (
    load_aws_credentials,
    create_bedrock_model_client,
)
from model_models import PlatformModelRequest


# Amazon Bedrock provider model IDs
BEDROCK_MODEL_FAMILIES = {
    "anthropic.claude": "Anthropic Claude",
    "ai21.j2": "AI21 Jurassic",
    "cohere.command": "Cohere Command",
    "meta.llama": "Meta Llama",
    "amazon.titan": "Amazon Titan",
    "mistral.mistral": "Mistral",
    "amazon.nova": "Amazon Nova",
}


def list_available_bedrock_models(
    region: str = "us-east-1",
    by_provider: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """List foundation models available on Amazon Bedrock.

    Uses boto3 to query the bedrock client for available foundation models,
    optionally filtered by provider family prefix.
    """
    credentials, _ = load_aws_credentials()
    bedrock_client = create_bedrock_model_client(credentials=credentials, region=region)

    list_kwargs: Dict[str, Any] = {"byInferenceType": "ON_DEMAND"}
    if by_provider:
        list_kwargs["byProvider"] = by_provider

    response = bedrock_client.list_foundation_models(**list_kwargs)
    models = response.get("modelSummaries", [])

    return [
        {
            "model_id": m.get("modelId"),
            "model_name": m.get("modelName"),
            "provider_name": m.get("providerName"),
            "input_modalities": m.get("inputModalities", []),
            "output_modalities": m.get("outputModalities", []),
            "response_streaming_supported": m.get("responseStreamingSupported", False),
        }
        for m in models
    ]


def resolve_bedrock_model(
    model_identifier: str,
    region: str = "us-east-1",
) -> Optional[Dict[str, Any]]:
    """Resolve a specific Bedrock model by identifier and return its details.

    Queries Amazon Bedrock to verify the model exists and returns metadata
    including model ARN and capabilities.
    """
    credentials, _ = load_aws_credentials()
    bedrock_client = create_bedrock_model_client(credentials=credentials, region=region)

    try:
        response = bedrock_client.get_foundation_model(modelIdentifier=model_identifier)
        model_data = response.get("modelDetails", {})
        return {
            "model_id": model_data.get("modelId"),
            "model_arn": model_data.get("modelArn"),
            "provider_name": model_data.get("providerName"),
            "model_name": model_data.get("modelName"),
            "input_modalities": model_data.get("inputModalities", []),
            "output_modalities": model_data.get("outputModalities", []),
            "customizations_supported": model_data.get("customizationsSupported", []),
            "inference_types_supported": model_data.get("inferenceTypesSupported", []),
        }
    except bedrock_client.exceptions.ResourceNotFoundException:
        return None


def select_default_text_model(
    region: str = "us-east-1",
) -> str:
    """Select a default text-generation model on Amazon Bedrock.

    Returns the model ID for Amazon Nova Micro, a cost-effective text model
    on Amazon Bedrock suitable for general text generation tasks.
    """
    default_model = "amazon.nova-micro-v1:0"

    resolved = resolve_bedrock_model(default_model, region=region)
    if resolved:
        return resolved["model_id"]

    fallback = "anthropic.claude-3-haiku-20240307-v1:0"
    return fallback


def create_model_request(
    prompt: str,
    system_prompt: Optional[str] = None,
    model_id: Optional[str] = None,
    region: str = "us-east-1",
    max_tokens: int = 1024,
    temperature: float = 0.7,
) -> PlatformModelRequest:
    """Create a normalized PlatformModelRequest after resolving the target model.

    Resolves the model identifier on Amazon Bedrock and builds a request
    configured for the platform.
    """
    if model_id is None:
        model_id = select_default_text_model(region=region)

    return PlatformModelRequest(
        model_id=model_id,
        system_prompt=system_prompt,
        user_message=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=0.9,
        stream=False,
    )
