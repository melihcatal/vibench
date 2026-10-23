import os
from openai import OpenAI
from model_client import get_platform_client


def select_platform_resource(
    resource_type: str = "model", criteria: dict = None
) -> str:
    """Resolves a provider-specific model, deployment, or inference resource before invocation."""
    client = get_platform_client()

    if resource_type == "model":
        return _select_model(criteria or {})
    elif resource_type == "deployment":
        return _select_deployment(criteria or {})
    else:
        raise ValueError(f"Unsupported resource type: {resource_type}")


def _select_model(criteria: dict) -> str:
    """Select appropriate OpenAI model based on criteria."""
    model_preference = criteria.get("preference", "balanced")

    model_map = {
        "balanced": "gpt-4o",
        "fast": "gpt-4o-mini",
        "powerful": "gpt-4-turbo",
        "cheap": "gpt-3.5-turbo",
    }

    selected_model = model_map.get(model_preference, "gpt-4o")

    if criteria.get("vision_required", False):
        selected_model = "gpt-4o"

    if criteria.get("context_length", 0) > 128000:
        selected_model = "gpt-4-turbo"

    return selected_model


def _select_deployment(criteria: dict) -> str:
    """Select deployment configuration for OpenAI models."""
    deployment_id = criteria.get("deployment_id")
    if deployment_id:
        return deployment_id

    model_name = _select_model(criteria)
    return f"{model_name}-deployment"
