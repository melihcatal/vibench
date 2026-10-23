# [HELPER] model_models.py
# Local request, response, and normalization utilities for Managed Model Platform Workflow

from typing import Dict, Any, List


def normalize_response(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Convert provider-agnostic raw response into a standardized shape.

    Expected standard fields:
        - normalized_text: the generated textual content
        - usage: optional usage metrics (tokens, cost)
        - resource_id: model or deployment identifier used
        - metadata: any additional provider-specific data retained under \"metadata\"
    """
    # Example: handle watsonx response
    normalized = {
        "normalized_text": raw.get("generated_text")
        or raw.get("content")
        or raw.get("text"),
        "usage": raw.get("usage")
        or raw.get("consumed_tokens")
        or raw.get("token_usage"),
        "resource_id": raw.get("resource_id")
        or raw.get("model_handle")
        or raw.get("model")
        or raw.get("deployment_id"),
        "metadata": raw.get("metadata") or {},
    }
    return normalized


def build_request(prompt: str, **kwargs) -> Dict[str, Any]:
    """Create a provider-neutral request payload.

    The dict can be passed directly into the client's invoke method after passing through a provider-specific adapter.
    """
    request = {
        "prompt": prompt,
        "parameters": kwargs,
    }
    return request
