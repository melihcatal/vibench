# model_models.py
# HELPER
# Define local request, response, and normalization helpers for Managed Model Platform Workflow

from typing import TypedDict, List, Any
from dataclasses import dataclass


class ModelInvocationRequest(TypedDict):
    project_id: str
    deployment_id: str
    input: str
    # Optional fields for advanced calls
    temperature: float = 0.7
    max_tokens: int = 256


@dataclass
class ModelInvocationResponse:
    output: str
    usage: Dict[str, int]  # e.g., {"prompt_tokens": 12, "completion_tokens": 8}


@dataclass
class StreamingChunk:
    text: str
    metadata: Dict[str, Any]  # provider-specific fields


@dataclass
class ResourceSpec:
    project_id: str
    type: str  # 'model' | 'deployment' | 'inference'
    name: str
    version: str = "latest"
    region: str = "default"


@dataclass
class ResourceLookupResult:
    resolved_id: str  # provider's internal resource identifier
    metadata: Dict[str, Any] = None


# Example normalization helper


def normalize_invocation_response(raw: Any) -> ModelInvocationResponse:
    """
    Convert provider-specific raw response into the standardized ModelInvocationResponse.
    """
    # Stub implementation – replace with actual mapping logic
    return ModelInvocationResponse(
        output=str(raw.get("output") or ""),
        usage=raw.get("usage", {}),
    )
