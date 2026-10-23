import os
from typing import Generic, TypeVar, Protocol

# Provider SDK placeholder – replace with real import for production
try:
    # Example for Azure OpenAI; other providers would have their own import path
    from openai import AzureOpenAI as _ProviderClient
except ImportError:
    # Minimal fake client for demonstration
    class _ProviderClient:
        def completions(self, deployment_id, prompt):
            return {"choices": [{"text": f"[Demo] Prompt processed for {deployment_id}"}]}

# Type aliases for generic model handling
def ModelId = str
TResponse = TypeVar("TResponse")

# Provider‑agnostic wrapper around the concrete SDK client
class ManagedModelClient(Generic[TResponse]):
    """Abstracts provider SDK initialization and request handling."""

    def __init__(self):
        self._client = _ProviderClient(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        )

    def invoke_model(self, request: "ModelInvocationRequest") -> TResponse:
        """Sync call using the underlying SDK."""
        # Unpack request assuming a generic provider supports a `completion`
        # method; adapt per provider as needed.
        return self._client.completions(
            deployment_id=request.resource_id,
            prompt=request.prompt,
        )

    def invoke_model_stream(self, request: "ModelInvocationRequest") -> "AsyncGenerator[ModelStreamChunk, None]":
        """Async streaming version – stubbed for illustration."""
        # Real SDKs expose an async generator or callback‑based stream.
        class _StubGenerator:
            def __aiter__(self):
                return self
            async def __anext__(self):
                return ModelStreamChunk(
                    raw_response={"done": False},
                    text="Streaming token..."
                )
        return _StubGenerator()

# Simple data‑classes for request/response contracts
class ModelInvocationRequest:
    def __init__(self, resource_id: str, prompt: str):
        self.resource_id = resource_id
        self.prompt = prompt

ModelStreamChunk = TypeVar("ModelStreamChunk")

class ModelStreamResponse(Protocol):
    raw_response: dict
    text: str
