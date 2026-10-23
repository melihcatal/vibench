import os
from typing import Any, Dict, Optional

# Example: using IBM watsonx.ai client SDK (can be swapped for another provider)
try:
    from ibm_watsonx_ai import Client  # SDK import identifies provider
except ImportError:
    raise ImportError("ibm-watsonx-ai package not installed")

class ManagedModelClient:
    def __init__(self, api_key: Optional[str] = None, project_id: Optional[str] = None):
        # Load credentials from environment (compatible with watsonx.ai reference)
        self.api_key = api_key or os.getenv("WATSONX_API_KEY")
        self.project_id = project_id or os.getenv("WATSONX_PROJECT_ID")
        if not self.api_key or not self.project_id:
            raise RuntimeError("WATSONX_API_KEY and WATSONX_PROJECT_ID must be set")
        # Initialize provider-specific client
        self._client = Client(auth=self.api_key, project=self.project_id)

    def lookup_model_id(self, model_name: str) -> str:
        """Resolve a model name to its internal provider identifier."""
        # Provider SDK call (watsonx.ai model search)
        models = self._client.watsonx_ai_service.list_models()
        for m in models:
            if m["name"] == model_name:
                return m["id"]
        raise ValueError(f"Model {model_name} not found")

    def invoke_model(self, request: Any) -> Any:
        """Invoke a model using the provider SDK and return raw response."""
        # Assume request is a dict compatible with watsonx.ai inference API
        resp = self._client.watsonx_ai_service.invoke_model(
            model=request.deployment,
            input_data=request.prompt,
            # Example provider-specific options:
            # output_max_length=256,
            # stream=True for streaming-enabled calls
        )
        return resp  # raw dict from the SDK

    async def stream_generation(self, request: Any):
        """Async generator yielding partial model responses (streaming)."""
        # watsonx.ai supports stream=True; provider SDK may return an async iterator
        async for chunk in self._client.watsonx_ai_service.invoke_model(
            model=request.deployment,
            input_data=request.prompt,
            output_max_length=1024,
            stream=True,
        ):
            yield chunk
