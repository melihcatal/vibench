import json
from typing import Dict, Any
from model_models import ModelInvocationResponse, PlatformMetadata

# Placeholder provider safety filter; in production this would call the provider's content
# moderation endpoint or use a third‑party library (e.g., OpenAI Moderation, Perspective API).


def is_safe(output: str, metadata: Dict[str, Any]) -> bool:
    """A naive safety check – replace with real moderation logic.

    Args:
        output: Model-generated text.
        metadata: Provider metadata (may include moderation flags).

    Returns:
        True if the output passes the safety filter, False otherwise.
    """
    # Example: treat any output containing disallowed keywords as unsafe
    unsafe_keywords = ["hate", "harassment", "self-harm", "sexual content"]
    lower_out = output.lower()
    for kw in unsafe_keywords:
        if kw in lower_out:
            return False
    # If provider metadata contains a moderation verdict, respect it
    if metadata.get("moderation", {}).get("flagged"):
        return False
    return True


def platform_output_safety(
    response: ModelInvocationResponse,
) -> ModelInvocationResponse:
    """Wraps an invocation response and adds a safety flag.

    Args:
        response: Original invocation result.

    Returns:
        Same response with an added `safe` boolean in the metadata.
    """
    safe = is_safe(response.output, response.metadata)
    # Safely merge metadata without mutating the original dict
    updated_meta = response.metadata.copy()
    updated_meta["safe"] = safe
    return ModelInvocationResponse(
        output=response.output,
        metadata=updated_meta,
    )
