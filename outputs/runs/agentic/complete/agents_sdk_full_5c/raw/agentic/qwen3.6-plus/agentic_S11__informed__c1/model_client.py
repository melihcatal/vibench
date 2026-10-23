"""Local configuration and client helper utilities for Managed Model Platform Workflow.

Uses Azure OpenAI Service as the primary provider.
"""

import os
from typing import Optional

from openai import AzureOpenAI


def get_azure_openai_endpoint() -> str:
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
    if not endpoint:
        raise ValueError("AZURE_OPENAI_ENDPOINT environment variable is not set")
    return endpoint.rstrip("/")


def get_azure_openai_api_key() -> str:
    api_key = os.environ.get("AZURE_OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("AZURE_OPENAI_API_KEY environment variable is not set")
    return api_key


def get_azure_openai_api_version() -> str:
    return os.environ.get("AZURE_OPENAI_API_VERSION", "2024-10-01-preview")


def get_default_deployment() -> str:
    deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
    return deployment


def create_azure_openai_client(
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
    api_version: Optional[str] = None,
) -> AzureOpenAI:
    """Create an AzureOpenAI SDK client scoped to the project/inference endpoint."""
    client = AzureOpenAI(
        azure_endpoint=endpoint or get_azure_openai_endpoint(),
        api_key=api_key or get_azure_openai_api_key(),
        api_version=api_version or get_azure_openai_api_version(),
    )
    return client


def build_system_prompt(
    task_description: str,
    output_format: Optional[str] = None,
    constraints: Optional[list[str]] = None,
) -> str:
    parts = [task_description]
    if output_format:
        parts.append(f"Format your response as: {output_format}")
    if constraints:
        for c in constraints:
            parts.append(f"Constraint: {c}")
    return "\n\n".join(parts)


def normalize_payload(
    prompt: str,
    deployment: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
    system_prompt: Optional[str] = None,
) -> dict:
    payload: dict = {
        "model": deployment or get_default_deployment(),
        "temperature": temperature,
        "max_tokens": max_tokens,
        "messages": [],
    }
    if system_prompt:
        payload["messages"].append({"role": "system", "content": system_prompt})
    payload["messages"].append({"role": "user", "content": prompt})
    return payload
