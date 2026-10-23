from typing import TypedDict, List

class ModelResource(TypedDict):
    """
    Provider‑agnostic representation of a resolved model/deployment.
    Contains the provider‑qualified ID and optional metadata such as model family.
    """
    resource_id: str
    model_family: str | None
    version_hint: str | None

class ModelInvocationMetadata(TypedDict):
    """
    Structure for the enriched response returned by `collect_platform_metadata`.
    """
    output: str
    usage: dict  # e.g., {"prompt_tokens": int, "completion_tokens": int, "total_tokens": int}
    model_handle: str
    request_id: str
    error: str | None

class ModelInvocationRequest(TypedDict):
    """
    Payload expected by `invoke_platform_model`, `stream_platform_generation`, etc.
    """
    resource_id: str
    prompt: str

# Optional helper for streamed chunks
class ModelStreamChunk(TypedDict):
    raw_response: dict
    text: str
