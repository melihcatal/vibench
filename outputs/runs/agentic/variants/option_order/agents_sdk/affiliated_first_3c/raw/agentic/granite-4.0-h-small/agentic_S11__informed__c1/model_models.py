from typing import NamedTuple, Optional

class ModelInvocationRequest(NamedTuple):
    """Normalized request passed to the high‑level client."""
    deployment_id: str
    prompt: str
    temperature: float = 0.7
    max_tokens: int = 256


class ModelInvocationResponse(NamedTuple):
    """Normalized response including both model output and provider metadata."""
    output: str
    usage: Optional[dict] = None
    resource_id: Optional[str] = None
    metadata: Optional[dict] = None


class ModelResourceRequest(NamedTuple):
    """Request to resolve a provider‑specific resource (model, deployment, etc.)."""
    name: str
    resource_type: str  # e.g., "model", "deployment", "inference"


class ModelResourceResponse(NamedTuple):
    """Resolved resource identifier from the provider."""
    id: str
    resource_type: str
    # Provider may add extra fields; kept open for extensions.


class ModelToken(NamedTuple):
    """Incremental token for streaming output."""
    text: str
    token_id: str = ""
    finish_reason: Optional[str] = None
