# [HELPER] model_models.py
# Define local request, response, and normalization helpers for Managed Model Platform Workflow

from typing import TypedDict, Dict, Any, List


class PromptInput(TypedDict):
    role: str
    content: str


class ProviderResponse(TypedDict):
    content: str
    usage: Dict[str, int]
    model: str
    request_id: str


class MetadataInfo(TypedDict):
    usage: Dict[str, int]
    model_id: str
    deployment_id: str
    request_id: str


class NormalizedResult(TypedDict):
    output: str
    metadata: MetadataInfo


class ProviderResource(TypedDict):
    """
    Helper type that can hold any of the resource identifiers a caller may provide.
    Exactly one of `model`, `deployment`, or `inference_profile` must be set.
    """

    model: str | None = None
    deployment: str | None = None
    inference_profile: str | None = None
