# [HELPER] model_models.py
# Define local request, response, and normalization helpers for Managed Model Platform Workflow

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field

# -----------------------------------------------------------------------------
# Request Models
# -----------------------------------------------------------------------------


@dataclass
class GenerationRequest:
    """Unified request payload for invoking a managed model."""

    deployment_id: str
    prompt: str
    max_tokens: Optional[int] = 256
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.95
    # Additional provider‑specific fields can be added as needed


# -----------------------------------------------------------------------------
# Normalized Response Models
# -----------------------------------------------------------------------------


@dataclass
class NormalizedResponse:
    """Standardised response payload returned by helper utilities."""

    output_text: str
    raw_response: Any  # provider‑specific original response object
    request_metadata: Dict[str, Any] = field(default_factory=dict)
    # Additional fields (e.g., completion tokens, logprobs) can be added


# -----------------------------------------------------------------------------
# Utility Functions
# -----------------------------------------------------------------------------


def normalize_response(raw: Any) -> str:
    """Extract the generated text from a watsonx.ai completion response."""
    # watsonx.ai returns a dict with a 'generated_text' key for each chunk
    # When streaming, each chunk is a dict; for non‑streaming we get a single dict
    if isinstance(raw, dict):
        return raw.get("generated_text", "")
    # Fallback for list of chunks (streaming case)
    if isinstance(raw, list):
        return "".join(chunk.get("generated_text", "") for chunk in raw)
    return ""


# -----------------------------------------------------------------------------
# Example Normalization Flow (illustrative)
# -----------------------------------------------------------------------------


def process_invocation(req: GenerationRequest) -> NormalizedResponse:
    """Invoke the client (via model_client.py) and return a normalized payload."""
    from model_client import get_client

    client = get_client()
    raw = client.invoke(req.deployment_id, req.prompt)
    text = normalize_response(raw["output"])
    metadata = {
        "request_id": raw["request_id"],
        "usage": raw.get("usage"),
    }
    return NormalizedResponse(
        output_text=text,
        raw_response=raw,
        request_metadata=metadata,
    )


# -----------------------------------------------------------------------------
# Module End
# -----------------------------------------------------------------------------
