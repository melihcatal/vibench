import os
import json
import asyncio
from typing import Dict, Any, Optional, Union, List

# Provider selection mapping
PROVIDER_CLIENT_MAP = {
    "azure_openai": "azure_ai_foundry_client.AzureOpenAIManagedClient",
}


class ManagedModelClient:
    """
    Unified client wrapper for provider‑specific Managed Model Platform APIs.

    The class delegates to a concrete client implementation based on the `provider`
    argument. All public methods (generate, stream_generate, normalize_response) are
    provider‑agnostic from the caller's perspective.

    Supports: Azure OpenAI (same‑scenario reference provider).
    """

    def __init__(
        self,
        endpoint: str,
        api_key: str,
        deployment_name: str,
        model_name: str,
        provider: str = "azure_openai",
    ):
        self.endpoint = endpoint
        self.api_key = api_key
        self.deployment_name = deployment_name
        self.model_name = model_name
        self.provider = provider
        # Dynamically import and instantiate the concrete client class
        mod_name, cls_name = PROVIDER_CLIENT_MAP[provider].rsplit(".", 1)
        module = __import__(mod_name, fromlist=[cls_name])
        self._client = getattr(module, cls_name)(
            endpoint=self.endpoint,
            api_key=self.api_key,
            deployment_name=self.deployment_name,
            model_name=self.model_name,
        )

    def generate(
        self,
        messages: List[Dict[str, Any]],
        temperature: float = 0.7,
        max_tokens: int = 100,
    ) -> Dict[str, Any]:
        """Synchronous generation call (calls the underlying async client)."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            self._client.generate(
                messages=messages, temperature=temperature, max_tokens=max_tokens
            )
        )
        loop.close()
        return result

    async def stream_generate(
        self, request_payload: Dict[str, Any]
    ) -> Union[Dict[str, Any], Any]:
        """
        Async generator that yields each raw chunk as returned by the provider SDK.
        """
        async for chunk in self._client.stream_generate(request_payload):
            yield chunk

    def normalize_response(self, raw_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert provider‑specific JSON payload into a standardized response shape:
          {
              "choices": [...],
              "usage": {...},
              "id": "...",
              "metadata": {...}
          }
        """
        # Azure OpenAI uses a slightly different envelope – normalize here
        if self.provider == "azure_openai":
            return {
                "choices": raw_response.get("choices", []),
                "usage": raw_response.get("usage"),
                "id": raw_response.get("id"),
                "metadata": raw_response.get("metadata", {}),
            }
        # Add adapters for other providers if needed
        return raw_response

    def close(self):
        # Placeholder – specific clients may need clean‑up (e.g., HTTP sessions)
        if hasattr(self._client, "close"):
            self._client.close()

    def __del__(self):
        self.close()
