from typing import TypedDict, Literal, Dict, Any


class InvocationRequest(TypedDict):
    prompt: str
    parameters: Dict[str, Any] | None


class InvocationResult(TypedDict):
    output: str
    failure: Literal[False] | Dict[str, Any]


class ProviderModelInfo(TypedDict):
    model_id: str
    provider: Literal["Hugging Face", "Amazon Bedrock", "Vertex AI"]


class NormalizedResponse(TypedDict):
    normalized_output: str
    provider_metadata: Dict[str, Any]
