import os
from typing import Any, Dict
# Choose one concrete provider via environment variables
if os.getenv('MODEL_PROVIDER') == 'azure':
    from azure.ai.foundry import FoundryClient  # Provider SDK import
    class ManagedModelClient:
        def __init__(self):
            endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
            api_key = os.getenv('AZURE_OPENAI_API_KEY')
            self.client = FoundryClient(endpoint=endpoint, api_key=api_key)
        def list_deployments(self) -> list[Dict[str, Any]]:
            return self.client.list_deployments()
        def invoke_generation(self, request) -> Any:
            # Adapts our request object to the SDK call
            return self.client.invoke(request.deployment, request.prompt,
                                      temperature=request.temperature,
                                      max_tokens=request.max_tokens,
                                      stream=request.stream)
        def stream_generation(self, request) -> Any:
            return self.client.stream(request.deployment, request.prompt,
                                      temperature=request.temperature,
                                      max_tokens=request.max_tokens)
else:
    # Fallback placeholder if no provider set (real implementation required for other providers)
    raise RuntimeError('MODEL_PROVIDER environment variable not configured')
