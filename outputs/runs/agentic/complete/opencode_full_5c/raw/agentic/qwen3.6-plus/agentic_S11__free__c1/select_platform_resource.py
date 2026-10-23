import os
from typing import Optional

from model_client import (
    get_bedrock_client,
    resolve_model_resource,
    KNOWN_BEDROCK_RESOURCES,
    DEFAULT_REGION,
)
from model_models import ModelResource


BEDROCK_MODEL_FAMILY_PREFIXES = {
    "anthropic.claude-3": "anthropic",
    "anthropic.claude": "anthropic",
    "amazon.titan-text": "amazon",
    "amazon.titan-embed": "amazon",
    "cohere.command": "cohere",
    "meta.llama": "meta",
    "mistral": "mistral",
}


def list_available_bedrock_models(
    region: Optional[str] = None,
    by_provider: Optional[str] = None,
    by_family: Optional[str] = None,
) -> list[ModelResource]:
    client = get_bedrock_client(region=region)
    paginator = client.get_paginator("list_foundation_models")
    resources: list[ModelResource] = []

    for page in paginator.paginate():
        models = page.get("modelSummaries", [])
        for model in models:
            model_id = model.get("modelId", "")
            if (
                by_provider
                and model.get("providerName", "").lower() != by_provider.lower()
            ):
                continue
            if by_family and by_family not in model_id:
                continue
            if not model.get("modelLifecycle", {}).get("status") == "ACTIVE":
                continue
            resource = ModelResource(
                model_id=model_id,
                model_arn=model.get("modelArn", ""),
                provider=model.get("providerName", "unknown"),
                model_family=_infer_family(model_id),
                supported_modalities=model.get("inputModalities", [])
                + model.get("outputModalities", []),
                max_input_tokens=model.get("maxTokens", {}).get("maximum", 0),
                max_output_tokens=model.get("maxTokens", {}).get("maximum", 0),
            )
            resources.append(resource)
    return resources


def select_platform_resource(
    model_id: Optional[str] = None,
    provider: Optional[str] = None,
    model_family: Optional[str] = None,
    region: Optional[str] = None,
) -> ModelResource:
    if model_id:
        if model_id in KNOWN_BEDROCK_RESOURCES:
            return KNOWN_BEDROCK_RESOURCES[model_id]
        resolved = resolve_model_resource(model_id)
        if resolved.provider != "unknown":
            return resolved

    candidates = list_available_bedrock_models(
        region=region,
        by_provider=provider,
        by_family=model_family,
    )

    if not candidates:
        return resolve_model_resource(model_id)

    if model_family:
        for candidate in candidates:
            if model_family in candidate.model_family:
                return candidate

    if provider:
        for candidate in candidates:
            if candidate.provider.lower() == provider.lower():
                return candidate

    return candidates[0]


def _infer_family(model_id: str) -> str:
    for prefix, family in BEDROCK_MODEL_FAMILY_PREFIXES.items():
        if model_id.startswith(prefix):
            return prefix
    return model_id.split(".")[0] if "." in model_id else model_id
