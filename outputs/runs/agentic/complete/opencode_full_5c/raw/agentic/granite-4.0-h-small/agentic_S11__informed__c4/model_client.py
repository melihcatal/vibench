# model_client.py
# [HELPER] local configuration and client helper utilities for Managed Model Platform Workflow

import os
from typing import Any, Dict, TypeVar

# Shared type for a generic model client (placeholder for any provider)
ClientT = TypeVar("ClientT")

# ---------------------------------------------------------------------------
# PROVIDER CONFIGURATION
# ---------------------------------------------------------------------------
# Detect preferred provider via environment variables.
# The example defaults to IBM watsonx.ai, but you can switch by setting
#   PROVIDER=vertexai | azure-openai | huggingface | bedrock | dashscope
PROVIDER = os.getenv("PROVIDER", "watsonx.ai")

# ---------------------------------------------------------------------------
# CLIENT CREATION FACTORY
# ---------------------------------------------------------------------------


def create_client() -> ClientT:
    """Return an initialized client instance for the selected provider."""
    if PROVIDER == "watsonx.ai":
        from ibm_watsonx_ai import Client

        return Client(
            url="https://api.watsonx.ibm.com",
            api_key=os.getenv("WATSONX_API_KEY"),
            project_id=os.getenv("WATSONX_PROJECT_ID"),
        )
    elif PROVIDER == "vertexai":
        from vertexai import generative_models

        return generative_models.GenerativeModel(
            model_name="gemini-1.5-pro",
            temperature=0.2,
        )
    elif PROVIDER == "azure-openai":
        from azure.ai.ml import (
            MLClient,
        )  # placeholder; actual Azure OpenAI SDK would be used

        # This is only a skeleton; real SDK usage would be added in production code.
        return MLClient.from_config()
    elif PROVIDER == "huggingface":
        from huggingface_hub import InferenceClient

        return InferenceClient(token=os.getenv("HF_TOKEN"))
    elif PROVIDER == "bedrock":
        import boto3

        return boto3.client(
            "bedrock-runtime",
            region_name="us-east-1",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )
    elif PROVIDER == "dashscope":
        import dashscope

        return dashscope.api.configure(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
        )
    else:
        raise ValueError(f"Unsupported provider: {PROVIDER}")


# ---------------------------------------------------------------------------
# UTILITY HELPERS
# ---------------------------------------------------------------------------


def normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize provider-agnostic payload to provider-specific shape."""
    # Placeholder: adjust key names, add required fields, etc.
    return payload


# Example usage (local only)
if __name__ == "__main__":
    client = create_client()
    print("Initialized client for provider:", PROVIDER)
