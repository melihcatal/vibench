import os
import openai
from typing import Any, Dict

class ManagedModelClient:
    """Thin wrapper around OpenAI Python SDK for managed model workflows.
    Loads provider-specific credentials from environment variables (e.g., OPENAI_API_KEY).
    Provides methods to call both synchronous and streaming endpoints.
    """

    def __init__(self):
        # Load provider-specific configuration; overrideable for tests
        self.openai_client = openai.AsyncClient(api_key=self._api_key())

    def _api_key(self) -> str:
        """Retrieve OpenAI API key from environment."""
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            raise RuntimeError("Missing OPENAI_API_KEY environment variable")
        return key

    async def _invoke_sync(self, model: str, prompt: str, **kwargs) -> Dict[str, Any]:
        """Synchronous OpenAI call wrapper."""
        return openai.ChatCompletion.create(model=model, messages=[{"role": "user", "content": prompt}], **kwargs)

    async def _invoke_stream(self, model: str, prompt: str, **kwargs) -> Any:
        """Streaming OpenAI call wrapper (async iterator)."""
        return openai.ChatCompletion.acreate(model=model, messages=[{"role": "user", "content": prompt}], stream=True, **kwargs)

    async def invoke_model(self, model: str, prompt: str, *, stream: bool = False, **kwargs) -> Any:
        """Unified entry point based on 'stream' flag."""
        if stream:
            return await self._invoke_stream(model, prompt, **kwargs)
        return await self._invoke_sync(model, prompt, **kwargs)

    async def stream_model(self, model: str, prompt: str, **kwargs):
        """Convenient streaming helper exposing async iterator."""
        async for chunk in self._invoke_stream(model, prompt, **kwargs):
            yield chunk

    def provider_name(self) -> str:
        """Return the concrete provider identifier recognized by the workflow."""
        return "openai"

    async def close(self):
        """Close underlying async client resources."""
        await self.openai_client.aclose()

# Example of use in other modules (see companion scripts for usage)
