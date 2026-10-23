"""[HELPER] model_client.py - Provide local configuration and client helper utilities for Managed Model Platform Workflow"""

import os


class ManagedModelClient:
    """Abstract base client that concrete provider clients will subclass."""

    def invoke(self, deployment_id: str, prompt: str, **kwargs):
        raise NotImplementedError

    def stream(self, deployment_id: str, prompt: str, chunk_size: int = 1024, **kwargs):
        """Default implementation yields a single chunk (non‑streaming)."""
        return [(self.invoke(deployment_id, prompt, **kwargs), None)]


def get_managed_model_client() -> ManagedModelClient:
    """
    Factory that returns a concrete provider client based on environment configuration.

    The concrete provider identifier is set via:
        * AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY (Amazon Bedrock)
        * GOOGLE_APPLICATION_CREDENTIALS (Vertex AI)
        * WATSONX_API_KEY / WATSONX_PROJECT_ID (IBM watsonx.ai)
        * DASHSCOPE_API_KEY (Alibaba DashScope)
        * AZURE_OPENAI_ENDPOINT / AZURE_OPENAI_API_KEY (Azure OpenAI)
        * HF_TOKEN (Hugging Face)

    Returns:
        An instance of the appropriate subclass.
    """
    # Detect provider via environment variables (simple heuristic)
    if os.getenv("AWS_ACCESS_KEY_ID") and os.getenv("AWS_SECRET_ACCESS_KEY"):
        from model_clients import AmazonBedrockClient

        return AmazonBedrockClient()
    elif os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        from model_clients import VertexAIModelClient

        return VertexAIModelClient()
    elif os.getenv("WATSONX_API_KEY") and os.getenv("WATSONX_PROJECT_ID"):
        from model_clients import WatsonXClient

        return WatsonXClient()
    elif os.getenv("DASHSCOPE_API_KEY"):
        from model_clients import DashScopeClient

        return DashScopeClient()
    elif os.getenv("AZURE_OPENAI_ENDPOINT") and os.getenv("AZURE_OPENAI_API_KEY"):
        from model_clients import AzureOpenAIModelClient

        return AzureOpenAIModelClient()
    elif os.getenv("HF_TOKEN"):
        from model_clients import HuggingFaceClient

        return HuggingFaceClient()
    else:
        raise RuntimeError(
            "No supported provider credentials found in environment variables."
        )
