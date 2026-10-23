# model_models.py
# [HELPER] Define local request, response, and normalization helpers for Managed Model Platform Workflow

from __future__ import annotations
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# REQUEST MODELS
# ---------------------------------------------------------------------------


class ModelInvocationRequest:
    """Normalized request payload that can be adapted for any provider."""

    def __init__(self, inputs: List[Any], deployment_id: Optional[str] = None):
        self.deployment_id = deployment_id
        self.inputs = inputs  # provider-agnostic list of input structures
        # Optional fields (e.g., temperature, max_tokens) can be added as needed
        self.params: Dict[str, Any] = {}

    def to_provider_specific(self) -> Dict[str, Any]:
        """Convert to the concrete provider payload."""
        # Example conversion for IBM watsonx.ai
        payload = {
            "inputs": self.inputs,
        }
        if self.deployment_id:
            payload["deployment_id"] = self.deployment_id
        # Merge any extra parameters (temperature, max_tokens, etc.)
        payload.update(self.params)
        return payload


# ---------------------------------------------------------------------------
# RESPONSE MODELS
# ---------------------------------------------------------------------------


class ModelInvocationResponse:
    """Response container that captures raw data and optional metadata."""

    def __init__(self, raw: Any, metadata: Optional[Dict[str, Any]] = None):
        self.raw = raw  # untouched provider response object
        self.metadata = metadata or {}

    def normalize_output(self) -> Any:
        """Extract the actual generated text/contents from the raw response."""
        # This is a generic placeholder; provider-specific subclasses can extend.
        return self.raw.get("output") or self.raw


# ---------------------------------------------------------------------------
# EXAMPLE PROVIDER-SPECIFIC ADAPTERS (optional)
# ---------------------------------------------------------------------------


class WatsonxResponseAdapter(ModelInvocationResponse):
    """Adapter for IBM watsonx.ai response structure."""

    def normalize_output(self) -> Any:
        # watsonx.ai returns {'output': {'generated_text': '...'}}
        return self.raw.get("output", {}).get("generated_text")

    def get_usage(self) -> Dict[str, Any]:
        return self.raw.get("usage") or {}


# ---------------------------------------------------------------------------
# USAGE ENTRIES POINT
# ---------------------------------------------------------------------------


def build_request(
    deployment_id: Optional[str] = None, **kwargs
) -> ModelInvocationRequest:
    """Utility to create a request with optional extra params."""
    req = ModelInvocationRequest(
        inputs=kwargs.pop("inputs", []), deployment_id=deployment_id
    )
    req.params = kwargs  # store extra parameters like temperature, top_p, etc.
    return req


# Example local test (no side effects)
if __name__ == "__main__":
    req = build_request(deployment_id="demo-model", inputs=["Hello", "world"])
    print("Normalized payload:", req.to_provider_specific())
