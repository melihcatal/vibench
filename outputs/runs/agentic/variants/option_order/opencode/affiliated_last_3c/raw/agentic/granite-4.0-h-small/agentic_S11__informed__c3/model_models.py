from typing import TypedDict, List, Any


class ModelInput(TypedDict):
    prompt: str
    temperature: float
    max_tokens: int


class ModelOutput(TypedDict):
    request_id: str
    content: str
    usage_estimate: str
    model_handle: str


class RequestMeta(TypedDict):
    provider: str
    resource_id: str
    payload: ModelInput


class NormalizedResponse(TypedDict):
    raw_response: Dict[str, Any]
    metadata: Dict[str, Any]


class StreamChunk(TypedDict):
    content: str
    metadata: Dict[str, Any]
