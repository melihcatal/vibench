# [HELPER] model_client.py
# Local configuration and client helper utilities for Managed Model Platform Workflow

import os
from model_models import ProviderResource

# ---------------------------------------------------------------------------
# Provider selection (choose one concrete service for the workflow)
# ---------------------------------------------------------------------------
# Example: Azure OpenAI Service
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_MODEL_NAME = os.getenv("AZURE_OPENAI_MODEL_NAME")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

# Optional fallback provider examples (commented out)
# HUGGINGFACE_TOKEN = os.getenv("HF_TOKEN")
# BEDROCK_ENDPOINT = os.getenv("BEDROCK_ENDPOINT")
# BEDROCK_API_KEY = os.getenv("BEDROCK_API_KEY")


class ManagedModelClient:
    """
    Thin wrapper that instantiates the provider SDK client and provides a unified
    `invoke`, `stream`, and `invoke_with_metadata` API surface.
    """

    def __init__(self):
        # Azure OpenAI SDK import
        from openai import AzureOpenAI

        self.client = AzureOpenAI(
            api_key=AZURE_OPENAI_API_KEY,
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            # provider‑specific defaults can be overridden per deployment
        )

    def invoke(self, project_id: str, deployment_id: str, payload: dict) -> dict:
        """Invoke a chat/completion endpoint and return raw response."""
        response = self.client.chat.completions.create(
            model=AZURE_OPENAI_MODEL_NAME,
            deployment_id=deployment_id,
            messages=[{"role": "user", "content": payload["input"]}],
            **payload.get("extra", {}),  # forward extra params if needed
        )
        return {
            "output": response.choices[0].message.content,
            "usage": response.usage,
            "model_id": response.model,
        }

    def stream(self, project_id: str, deployment_id: str, messages: list) -> list:
        """Streaming invocation returning a list of chunk dicts."""
        chunks = []
        # Async‐compatible streaming; for simplicity we iterate over the generator
        async_resp = self.client.chat.completions.create(
            model=AZURE_OPENAI_MODEL_NAME,
            deployment_id=deployment_id,
            messages=messages,
            stream=True,
        )
        for chunk in async_resp.stream():  # type: ignore
            # chunk.choices[0].delta.content holds the streamed token text
            chunk_text = getattr(chunk.choices[0].delta, "content", "")
            chunks.append({"content": chunk_text})
        return chunks

    def invoke_with_metadata(
        self, project_id: str, deployment_id: str, payload: dict
    ) -> dict:
        """Invoke and also collect provider‑specific metadata."""
        raw = self.client.chat.completions.create(
            model=AZURE_OPENAI_MODEL_NAME,
            deployment_id=deployment_id,
            messages=[{"role": "user", "content": payload["input"]}],
            response_format={"type": "text"},
        )
        # The OpenAI SDK surfaces usage and other metadata directly on the response
        return {
            "output": raw.choices[0].message.content,
            "metadata": {
                "usage": raw.usage,
                "model_id": raw.model,
                "request_id": raw.request_id,
            },
        }
