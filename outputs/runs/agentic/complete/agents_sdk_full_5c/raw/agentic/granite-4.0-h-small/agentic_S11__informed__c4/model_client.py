import os
from typing import Any, Dict, Optional

# Placeholder for concrete SDK imports; select at runtime based on env variable
# Example: for Vertex AI -> from vertexai import language_models
#            for Azure OpenAI -> from azure.ai.openai import OpenAIClient
#            for watsonx -> from ibm_watsonx_ai.services import WatsonxLLMService

ModelDescriptor = Dict[str, Any]


class ManagedModelClient:
    """
    High‑level helper that hides the underlying provider SDK.
    The class is instantiated with no arguments; it reads environment variables
    to decide which provider SDK to load and creates a ready‑to‑use client.
    """

    def __init__(self):
        self._client = self._initialize_sdk()

    def _initialize_sdk(self) -> Any:
        # Choose provider based on environment
        platform = os.getenv('MODEL_PLATFORM', 'vertexai').lower()
        if platform == 'vertexai':
            from vertexai import language_models
            # Set up Google Cloud credentials (usually GOOGLE_APPLICATION_CREDENTIALS env var)
            return language_models.LanguageModelClient()
        elif platform == 'azureopenai':
            from azure.ai.openai import OpenAIClient
            endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
            api_key = os.getenv('AZURE_OPENAI_API_KEY')
            deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gemma')
            return OpenAIClient(endpoint=endpoint, api_key=api_key, deployment_name=deployment)
        elif platform == 'watsonx':
            from ibm_watsonx_ai.services import WatsonxLLMService
            project_id = os.getenv('WATSONX_PROJECT_ID')
            api_key = os.getenv('WATSONX_API_KEY')
            return WatsonxLLMService(project_id=project_id, api_key=api_key)
        else:
            raise RuntimeError('Unsupported MODEL_PLATFORM: ' + platform)

    async def invoke(self, request: Any) -> Any:
        """Synchronous wrapper; for async providers use the async client directly."""
        return self._client.invoke(request)

    async def stream_generate(self, request: Any):
        """Async streaming generation where supported."""
        return self._client.stream_generate(request)

    def close(self):
        # Close client if the SDK provides a close method
        if hasattr(self._client, 'close'):
            self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
