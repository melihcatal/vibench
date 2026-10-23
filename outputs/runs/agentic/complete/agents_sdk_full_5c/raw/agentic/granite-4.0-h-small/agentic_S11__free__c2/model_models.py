# [HELPER] model_models.py
from typing import Any, Dict, Generic, TypeVar, NamedTuple, List

# Request/response models for the platform workflow. Adjust fields as required by the provider.

# Provider-specific request types can be imported from the SDK if available.
# Example: from openai import OpenAIChatRequest  # <-- provider-specific

# Generic base classes for request/response templates
T = TypeVar('T')

class BaseRequest(NamedTuple):
    deployment_id: str
    prompt: str
    temperature: float = 0.0
    max_tokens: int = 256
    # add other provider‑specific parameters as needed

    @property
    def raw(self) -> Dict[str, Any]:
        # Convert the typed fields to the plain dict expected by the SDK / API.
        return {
            'model': self.deployment_id,
            'prompt': self.prompt,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens,
            # include additional fields required by the provider
        }

class ModelInvocationRequest(BaseRequest):
    """Typed request object for a synchronous model invocation."""

class ModelStreamInvocationRequest(BaseRequest):
    """Typed request object for a streaming model invocation."""

class BaseResponse(NamedTuple):
    text: str
    usage: Dict[str, int]
    # Provider‑specific metadata can be added here, e.g., 'resource_id', 'request_id', etc.

    @property
    def raw(self) -> Dict[str, Any]:
        # By default return a stub; subclasses will fill in real provider data.
        return {'choices': [{'message': {'role': 'assistant', 'content': self.text}}]}

class ModelInvocationResponse(BaseResponse):
    """Response from a synchronous invocation, includes full provider metadata."""

    def __new__(cls, *args, **kwargs):
        # Allow downstream code to attach extra provider fields without breaking immutability.
        obj = super().__new__(cls, *args, **kwargs)
        obj.raw = kwargs.get('raw', {'choices': [{'message': {'role': 'assistant', 'content': obj.text}}]})
        return obj

class StreamResponseChunk(NamedTuple):
    text: str
    raw: Dict[str, Any]

# Example usage (uncomment for testing)
# if __name__ == '__main__':
#     req = ModelInvocationRequest(deployment_id='test-dep', prompt='Hello')
#     resp = ModelInvocationResponse(text=req.prompt, usage={'prompt_tokens': 0})
#     print(resp)
