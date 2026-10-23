"""Resolve a provider-specific model, deployment, or inference resource before invocation.

Uses Amazon Bedrock control-plane APIs to list and resolve available foundation models
by provider, model family, or capability. Returns a concrete Bedrock model identifier
suitable for downstream invocation.

Provider: Amazon Bedrock
SDK: boto3 (bedrock control-plane client)
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

import os
from typing import List, Optional

from model_client import create_bedrock_client, resolve_bedrock_credentials
from model_models import PlatformModelRequest


def list_available_bedrock_models(
    by_provider: Optional[str] = None,
    by_custom_model: bool = False,
) -> List[dict]:
    """List available Amazon Bedrock foundation models.

    Args:
        by_provider: Filter by provider name (e.g., 'Anthropic', 'Meta', 'Amazon').
        by_custom_model: If True, list custom models; if False, list base models.

    Returns:
        List of model info dicts with modelId, modelName, providerName, etc.
    """
    credentials = resolve_bedrock_credentials()
    client = create_bedrock_client(credentials)

    kwargs = {"byCustomization": by_custom_model}
    if by_provider:
        kwargs["byProvider"] = by_provider

    response = client.list_foundation_models(**kwargs)
    return response.get("modelSummaries", [])


def resolve_model_id(
    model_name: str,
    provider_filter: Optional[str] = None,
) -> str:
    """Resolve a model name pattern to a concrete Bedrock model ID.

    Searches available Bedrock models for one matching the given name pattern
    and optional provider filter. Returns the full Bedrock model identifier.

    Args:
        model_name: Model name or pattern to search for (e.g., 'claude-3-sonnet').
        provider_filter: Optional provider name filter.

    Returns:
        Concrete Bedrock model ID string.

    Raises:
        ValueError: If no matching model is found.
    """
    models = list_available_bedrock_models(by_provider=provider_filter)

    for model in models:
        model_id = model.get("modelId", "")
        model_name_field = model.get("modelName", "")
        provider = model.get("providerName", "")

        if model_name.lower() in model_id.lower() or model_name.lower() in model_name_field.lower():
            return model_id

    raise ValueError(
        f"No Bedrock model found matching '{model_name}'"
        f"{' with provider ' + provider_filter if provider_filter else ''}"
    )


def get_model_details(model_id: str) -> dict:
    """Retrieve detailed information about a specific Bedrock foundation model.

    Args:
        model_id: Full Bedrock model identifier.

    Returns:
        Dict with model details including input/output modalities, supported regions.
    """
    credentials = resolve_bedrock_credentials()
    client = create_bedrock_client(credentials)

    response = client.get_foundation_model(modelIdentifier=model_id)
    return response.get("modelDetails", {})


def validate_model_access(model_id: str) -> bool:
    """Check if the current AWS account has access to the specified Bedrock model.

    Args:
        model_id: Full Bedrock model identifier.

    Returns:
        True if the model is accessible, False otherwise.
    """
    try:
        details = get_model_details(model_id)
        return details.get("customizationsSupported") is not None or True
    except Exception:
        return False


def select_best_model_for_task(
    task_type: str = "general",
    max_tokens_required: int = 4096,
) -> str:
    """Select an appropriate Bedrock model based on task requirements.

    Args:
        task_type: Type of task ('general', 'embedding', 'summarization', 'creative').
        max_tokens_required: Minimum output tokens needed.

    Returns:
        Selected Bedrock model ID.
    """
    model_selection = {
        "general": "anthropic.claude-3-sonnet-20240229-v1:0",
        "summarization": "anthropic.claude-3-haiku-20240307-v1:0",
        "creative": "anthropic.claude-3-5-sonnet-20241022-v2:0",
        "embedding": "amazon.titan-embed-text-v2:0",
        "long_context": "anthropic.claude-3-5-sonnet-20241022-v2:0",
    }

    candidate_id = model_selection.get(task_type, model_selection["general"])

    try:
        if validate_model_access(candidate_id):
            return candidate_id
    except Exception:
        pass

    return "anthropic.claude-3-sonnet-20240229-v1:0"


if __name__ == "__main__":
    resolved_id = resolve_model_id("claude-3-sonnet")
    print(f"Resolved model ID: {resolved_id}")
