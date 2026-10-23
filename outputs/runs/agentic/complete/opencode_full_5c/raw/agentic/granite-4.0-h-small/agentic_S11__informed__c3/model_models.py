# model_models.py
# HELPER: request, response, and normalization utilities for Managed Model Platform Workflow

from typing import Any, Dict


def parse_response(raw: Any) -> Dict[str, Any]:
    """Convert a provider's raw response into a standardized dict."""
    # Detect provider from raw payload and parse accordingly
    if isinstance(raw, dict) and "choices" in raw:
        # OpenAI / Azure OpenAI style
        return {
            "choices": raw["choices"],
            "usage": raw.get("usage"),
            "metadata": raw.get("metadata"),
        }
    elif isinstance(raw, dict) and "model" in raw:
        # Bedrock style (single choice, text output directly)
        return {
            "text": raw.get("text"),
            "model": raw.get("model"),
            "usage": raw.get("usage"),
        }
    elif isinstance(raw, dict) and "candidates" in raw:
        # Vertex AI generative style
        return {
            "candidates": raw["candidates"],
            "response_metadata": raw.get("responseMetadata"),
        }
    # Simple fallback
    return {"raw_text": str(raw)}


def build_request_payload(
    model: str,
    deployment: str,
    profile: str,
    user_input: str,
) -> Dict[str, Any]:
    """Create a provider‑agnostic request payload."""
    payload = {
        "model": model,
        "deployment": deployment,
        "profile": profile,
        "input": {
            "text": user_input,
        },
    }
    # Add provider‑specific fields here if needed
    return payload


def add_safety_flags(payload: Dict[str, Any], flags: Dict[str, Any]) -> None:
    """Merge safety‑related flags into the payload."""
    # Example for Bedrock guardrails
    if infer_provider_name() == "aws":
        payload["guardrails"] = flags
    # Placeholder for other providers
    pass


def enable_streaming(payload: Dict[str, Any]) -> None:
    """Turn on streaming for supported providers."""
    if infer_provider_name() == "aws":
        payload["stream"] = True
    # Placeholder for other providers
    pass
