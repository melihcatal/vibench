"""Returns model output together with provider platform metadata such as usage, resource IDs, or model handles.

Provider: Azure OpenAI Service (https://learn.microsoft.com/azure/ai-services/openai/)
SDK: openai >= 1.0.0 with AzureOpenAI client class.
Collects Azure-specific metadata: usage tokens, system_fingerprint, request_id,
prompt_filter_results, content_filter_results, and deployment model mapping.
"""

from __future__ import annotations

from typing import Optional, Any

from openai import AzureOpenAI

from model_client import build_azure_openai_client
from model_models import (
    PlatformRequest,
    PlatformResponse,
    PlatformUsage,
    normalize_messages,
)


def collect_platform_metadata(
    *,
    prompt: str,
    deployment_id: str,
    client: Optional[AzureOpenAI] = None,
    system_prompt: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 1024,
) -> dict[str, Any]:
    """Invoke an Azure OpenAI model and return output with full provider metadata.

    The returned dict includes:
    - content: The model's text output
    - usage: Token usage (prompt, completion, total) from Azure OpenAI
    - model_id: Azure OpenAI model/deployment identifier
    - request_id: Azure provider request tracking ID
    - system_fingerprint: Azure OpenAI system fingerprint
    - prompt_filter_results: Azure content safety results for the prompt
    - content_filter_results: Azure content safety results for the output
    - deployment_details: Resource-level deployment metadata
    - provider: Provider identifier ("azure_openai")

    Args:
        prompt: The user input text.
        deployment_id: Azure OpenAI deployment name.
        client: Pre-built AzureOpenAI client. Built automatically if not provided.
        system_prompt: Optional system prompt.
        temperature: Sampling temperature.
        max_tokens: Maximum tokens to generate.

    Returns:
        Dict combining model output and all available Azure platform metadata.
    """
    if client is None:
        client = build_azure_openai_client()

    messages = normalize_messages(prompt, system_prompt=system_prompt)

    response = client.chat.completions.create(
        model=deployment_id,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    normalized = PlatformResponse.from_azure_response(response)

    # Collect deployment-level resource metadata
    deployment_details = {}
    try:
        model_info = client.models.get(deployment_id)
        deployment_details = {
            "deployment_id": model_info.id,
            "model_name": getattr(model_info, "model", None),
            "status": getattr(model_info, "status", None),
            "created_at": getattr(model_info, "created_at", None),
        }
    except Exception:
        deployment_details = {
            "deployment_id": deployment_id,
            "error": "Could not fetch deployment details",
        }

    # Extract Azure-specific usage metadata
    usage_data = {}
    if response.usage:
        usage_data = {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        }

    # Extract Azure provider-specific request metadata
    request_id = getattr(response, "request_id", None)
    system_fingerprint = getattr(response, "system_fingerprint", None)

    # Extract Azure-specific content filter results
    prompt_filter = None
    if hasattr(response, "prompt_filter_results") and response.prompt_filter_results:
        prompt_filter = [
            f.as_dict() if hasattr(f, "as_dict") else str(f)
            for f in response.prompt_filter_results
        ]

    content_filter = None
    if response.choices and hasattr(response.choices[0], "content_filter_results"):
        cfr = response.choices[0].content_filter_results
        if cfr:
            content_filter = (
                cfr.as_dict() if hasattr(cfr, "as_dict") else str(cfr)
            )

    metadata = {
        "provider": "azure_openai",
        "content": normalized.content,
        "finish_reason": normalized.finish_reason,
        "model_id": normalized.model_id,
        "deployment_id": deployment_id,
        "usage": usage_data,
        "request_id": request_id,
        "system_fingerprint": system_fingerprint,
        "prompt_filter_results": prompt_filter,
        "content_filter_results": content_filter,
        "deployment_details": deployment_details,
    }

    return metadata


def collect_streaming_metadata(
    *,
    prompt: str,
    deployment_id: str,
    client: Optional[AzureOpenAI] = None,
    system_prompt: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
) -> dict[str, Any]:
    """Stream an Azure OpenAI response and collect full metadata from the final chunk.

    Azure OpenAI streaming responses only include usage metadata in the final
    chunk. This function accumulates text content and extracts all available
    metadata from the stream.

    Args:
        prompt: The user input text.
        deployment_id: Azure OpenAI deployment name.
        client: Pre-built AzureOpenAI client. Built automatically if not provided.
        system_prompt: Optional system prompt.
        temperature: Sampling temperature.
        max_tokens: Maximum tokens to generate.

    Returns:
        Dict combining accumulated model output and provider metadata.
    """
    if client is None:
        client = build_azure_openai_client()

    messages = normalize_messages(prompt, system_prompt=system_prompt)

    stream = client.chat.completions.create(
        model=deployment_id,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True,
    )

    accumulated_text = []
    last_chunk = None

    for chunk in stream:
        last_chunk = chunk
        if chunk.choices and chunk.choices[0].delta.content:
            accumulated_text.append(chunk.choices[0].delta.content)

    full_text = "".join(accumulated_text)

    # Extract metadata from the final chunk (Azure provides usage only here)
    model_id = getattr(last_chunk, "model", deployment_id) if last_chunk else deployment_id
    system_fingerprint = getattr(last_chunk, "system_fingerprint", None)
    finish_reason = (
        last_chunk.choices[0].finish_reason
        if last_chunk and last_chunk.choices
        else "unknown"
    )

    usage_data = {}
    if last_chunk and getattr(last_chunk, "usage", None):
        usage_data = {
            "prompt_tokens": last_chunk.usage.prompt_tokens,
            "completion_tokens": last_chunk.usage.completion_tokens,
            "total_tokens": last_chunk.usage.total_tokens,
        }

    return {
        "provider": "azure_openai",
        "content": full_text,
        "model_id": model_id,
        "deployment_id": deployment_id,
        "usage": usage_data,
        "system_fingerprint": system_fingerprint,
        "finish_reason": finish_reason,
    }
