# [HELPER] model_client.py
# Local configuration and client utilities for Managed Model Platform Workflow

import os
from typing import Optional


def get_client(preferred_service: str = "watsonx"):
    """Return a configured client instance for a given managed model platform.

    Args:
        preferred_service: Identifier for the provider (default: watsonx). Supported: watsonx, huggingface, bedrock, vertex, dashscope, azure.
    """
    if preferred_service == "watsonx":
        api_key = os.getenv("WATSONX_API_KEY")
        project_id = os.getenv("WATSONX_PROJECT_ID")
        if not api_key or not project_id:
            raise ValueError(
                "Set WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables"
            )
        from ibm_watsonx_ai import APIClient

        return APIClient(api_key=api_key, project_id=project_id)
    elif preferred_service == "huggingface":
        token = os.getenv("HF_TOKEN")
        if not token:
            raise ValueError("Set HF_TOKEN environment variable")
        from huggingface_hub import HfApi, HfFileSystem

        return HfApi(token=token)
    elif preferred_service == "bedrock":
        # boto3 client for Amazon Bedrock; credentials via standard AWS env vars
        import boto3

        return boto3.client("bedrock-runtime")
    elif preferred_service == "vertex":
        # Vertex AI generative models; uses GOOGLE_APPLICATION_CREDENTIALS
        from vertexai.preview.generative_ai import GenerativeModel

        return GenerativeModel
    elif preferred_service == "dashscope":
        # DashScope SDK; DASHSCOPE_API_KEY env var
        import dashscope

        return dashscope
    elif preferred_service == "azure":
        # Azure OpenAI client; AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY env vars
        from azure.ai.openai import OpenAIClient

        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        key = os.getenv("AZURE_OPENAI_API_KEY")
        if not endpoint or not key:
            raise ValueError(
                "Set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY environment variables"
            )
        return OpenAIClient(endpoint=endpoint, credential=key)
    else:
        raise ValueError(f"Unsupported preferred_service: {preferred_service}")
