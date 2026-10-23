"""
[SAME-SCENARIO] Resolves a provider-specific model, deployment, or inference
resource before invocation on Amazon Bedrock.

Provider: Amazon Bedrock
SDK: boto3
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

from __future__ import annotations

import os
from typing import Optional

from model_client import get_bedrock_client, resolve_model_id


# Provider-specific Bedrock model availability categories
FOUNDATION_MODEL_STATUS = "ACTIVE"
CUSTOM_MODEL_STATUS = "ACTIVE"
PROVISIONED_THROUGHPUT_STATUS = "ACTIVE"


def list_available_foundation_models(
    region: Optional[str] = None,
    by_provider: Optional[str] = None,
    by_output_modality: Optional[str] = None,
) -> list[dict]:
    """List available foundation models on Amazon Bedrock.

    Uses boto3 bedrock client's list_foundation_models API.
    Provider signals: boto3, bedrock client, Bedrock-specific filter parameters.
    """
    bedrock = get_bedrock_client(region_name=region)

    params = {"byInferenceType": "ON_DEMAND"}
    if by_provider:
        params["byProvider"] = by_provider
    if by_output_modality:
        params["byOutputModality"] = by_output_modality

    response = bedrock.list_foundation_models(**params)
    return response.get("modelSummaries", [])


def get_model_details(model_id: str, region: Optional[str] = None) -> dict:
    """Retrieve detailed information for a specific Amazon Bedrock model.

    Provider signals: boto3 bedrock.get_foundation_model, Bedrock modelId format.
    """
    bedrock = get_bedrock_client(region_name=region)
    response = bedrock.get_foundation_model(modelIdentifier=model_id)
    return response.get("modelDetails", {})


def resolve_best_model_for_task(
    task_description: str,
    region: Optional[str] = None,
) -> str:
    """Resolve the best Amazon Bedrock model ID for a given task description.

    Uses provider-specific model metadata (input/output modalities, response
    streaming support, customizations supported) to select an appropriate model.

    Provider signals: Bedrock model selection logic using Bedrock-specific
    model identifiers like anthropic.claude-3-5-sonnet-20241022-v2:0.
    """
    models = list_available_foundation_models(region=region)

    text_models = [
        m for m in models
        if m.get("outputModalities", []) == ["TEXT"]
        and m.get("modelLifecycle", {}).get("status") == FOUNDATION_MODEL_STATUS
    ]

    task_lower = task_description.lower()

    # Heuristic selection based on Bedrock model capabilities
    if any(kw in task_lower for kw in ["complex", "reasoning", "analysis", "detailed"]):
        candidates = [
            m for m in text_models
            if "claude-3-5-sonnet" in m.get("modelId", "")
            or "claude-3-sonnet" in m.get("modelId", "")
        ]
        if candidates:
            return candidates[0]["modelId"]

    if any(kw in task_lower for kw in ["fast", "simple", "quick", "brief"]):
        candidates = [
            m for m in text_models
            if "haiku" in m.get("modelId", "")
        ]
        if candidates:
            return candidates[0]["modelId"]

    # Default to a strong general-purpose Bedrock model
    for m in text_models:
        mid = m.get("modelId", "")
        if "claude-3-5-sonnet" in mid or "llama3-70b" in mid:
            return mid

    # Fallback to first available text model
    if text_models:
        return text_models[0]["modelId"]

    raise RuntimeError("No suitable Amazon Bedrock foundation model found")


def get_provisioned_throughput_details(
    arn: str,
    region: Optional[str] = None,
) -> dict:
    """Get details of a provisioned throughput resource on Amazon Bedrock.

    Provider signals: boto3 bedrock.get_provisioned_model_throughput,
    Bedrock ARN-based resource identifiers.
    """
    bedrock = get_bedrock_client(region_name=region)
    response = bedrock.get_provisioned_model_throughput(provisionedModelId=arn)
    return response


def list_custom_models(region: Optional[str] = None) -> list[dict]:
    """List custom (fine-tuned) models available in Amazon Bedrock.

    Provider signals: boto3 bedrock.list_custom_models, Bedrock custom model API.
    """
    bedrock = get_bedrock_client(region_name=region)
    response = bedrock.list_custom_models()
    return response.get("modelSummaries", [])


def select_resource(
    task: str = "general text generation",
    region: Optional[str] = None,
    prefer_model: Optional[str] = None,
) -> dict:
    """Main entry point: select a Bedrock resource for invocation.

    Returns a dict with the resolved model ID and resource metadata.
    Provider: Amazon Bedrock, model identifiers like
    anthropic.claude-3-5-sonnet-20241022-v2:0.
    """
    if prefer_model:
        model_id = resolve_model_id(prefer_model)
        details = get_model_details(model_id, region=region)
        return {
            "model_id": model_id,
            "provider": "amazon-bedrock",
            "details": details,
            "resource_type": "foundation_model",
        }

    model_id = resolve_best_model_for_task(task, region=region)
    details = get_model_details(model_id, region=region)
    return {
        "model_id": model_id,
        "provider": "amazon-bedrock",
        "details": details,
        "resource_type": "foundation_model",
    }
