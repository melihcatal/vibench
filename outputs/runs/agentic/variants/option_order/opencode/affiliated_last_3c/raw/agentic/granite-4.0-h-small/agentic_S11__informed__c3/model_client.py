import os
from typing import Dict, Any


class ManagedModelClient:
    """Local configuration and client helper utilities for Managed Model Platform Workflow."""

    def __init__(self):
        # Detect service from environment variables (only one provider is implemented for demo)
        if self._has_env("AWS_ACCESS_KEY_ID"):
            self.service = "Amazon Bedrock"
            self.region = os.getenv("AWS_REGION", "us-east-1")
        elif self._has_env("GOOGLE_APPLICATION_CREDENTIALS"):
            self.service = "Vertex AI"
            self.region = "global"
        elif self._has_env("DASHSCOPE_API_KEY"):
            self.service = "Alibaba Model Studio"
            self.region = os.getenv("ALIBABA_CLOUD_REGION", "cn-hangzhou")
        elif self._has_env("AZURE_OPENAI_ENDPOINT"):
            self.service = "Azure OpenAI"
            self.region = os.getenv("AZURE_OPENAI_REGION", "eastus")
        elif self._has_env("HF_TOKEN"):
            self.service = "Hugging Face"
            self.region = "hf.co"
        elif self._has_env("WATSONX_API_KEY"):
            self.service = "IBM watsonx.ai"
            self.region = os.getenv("WATSONX_PROJECT_ID", "default-project")
        else:
            raise RuntimeError("Missing required credentials for a supported provider.")

    @staticmethod
    def _has_env(var: str) -> bool:
        return var in os.environ and os.environ[var] != ""

    def invoke(self, resource_id: str, payload: dict) -> dict:
        """Generic invoke wrapper – replace with real SDK calls per provider."""
        # Placeholder: return a dict that mimics a generic provider response
        return {
            "request_id": f"{self.service.replace(' ', '_')}-request-{id(self)}",
            "content": f"[simulated response for {resource_id}] {payload.get('prompt', '')}",
            "usage_estimate": "0.001",
            "model_handle": resource_id,
        }

    def stream(self, resource_id: str, prompt: str):
        """Placeholder generator that yields a single chunk to simulate streaming."""
        yield {
            "content": f"[simulated streaming for {resource_id}] {prompt}",
            "id": "stream-chunk-1",
            "token_count": 12,
            "finish_reason": None,
        }
