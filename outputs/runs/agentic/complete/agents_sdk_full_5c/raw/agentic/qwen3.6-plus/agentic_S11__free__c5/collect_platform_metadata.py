"""
[SAME-SCENARIO] Returns model output together with provider platform metadata
such as usage, resource IDs, or model handles from the Azure OpenAI platform.

Collects and packages the full response metadata returned by the
Azure OpenAI managed model service, including token usage, model identifiers,
system fingerprints, and content filter results.
"""

from __future__ import annotations

from typing import Optional

from openai import AzureOpenAI

from model_models import PlatformModelRequest, PlatformModelResponse, PlatformMetadata
from model_client import (
    get_azure_openai_client,
    build_messages,
    extract_text_from_completion,
    extract_token_usage,
)
from select_platform_resource import resolve_deployment_for_request


def collect_platform_metadata(
    request: PlatformModelRequest,
    client: Optional[AzureOpenAI] = None,
) -> PlatformModelResponse:
    """
    Invoke an Azure OpenAI managed model and return output with full platform metadata.

    Makes a chat completion request to Azure OpenAI and captures all provider
    metadata including model ID, usage statistics, request ID, system fingerprint,
    and content filter results.

    Args:
        request: PlatformModelRequest with deployment and content configuration.
        client: Optional pre-configured AzureOpenAI client.

    Returns:
        PlatformModelResponse with content and comprehensive provider metadata.
    """
    if client is None:
        client = get_azure_openai_client()

    resolved_deployment, model_config = resolve_deployment_for_request(request, client)

    messages = build_messages(request.system_prompt, request.user_content)

    kwargs: dict = {
        "model": resolved_deployment,
        "messages": messages,
        "temperature": request.temperature,
        "top_p": request.top_p,
    }
    if request.max_tokens is not None:
        kwargs["max_tokens"] = request.max_tokens
    if request.stop is not None:
        kwargs["stop"] = request.stop
    if request.extra_body is not None:
        kwargs["extra_body"] = request.extra_body

    response = client.chat.completions.create(**kwargs)

    content = extract_text_from_completion(response)
    usage = extract_token_usage(response)

    # Extract Azure OpenAI specific metadata
    model_id = getattr(response, "model", resolved_deployment)
    request_id = None
    if hasattr(response, "_request_id"):
        request_id = response._request_id
    elif hasattr(response, "id"):
        request_id = response.id

    system_fingerprint = getattr(response, "system_fingerprint", None)
    created_timestamp = getattr(response, "created", None)

    # Extract content filter results from Azure OpenAI response
    content_filter_results = None
    if response.choices and len(response.choices) > 0:
        choice = response.choices[0]
        if hasattr(choice, "content_filter_results"):
            content_filter_results = choice.content_filter_results
        # Also check for Azure-specific filter attributes in message
        message = getattr(choice, "message", None)
        if message and hasattr(message, "content_filter_results"):
            content_filter_results = message.content_filter_results

    finish_reason = None
    if response.choices and len(response.choices) > 0:
        finish_reason = response.choices[0].finish_reason

    metadata = PlatformMetadata(
        model_id=model_id,
        deployment_name=resolved_deployment,
        created_timestamp=created_timestamp,
        system_fingerprint=system_fingerprint,
        prompt_tokens=usage.get("prompt_tokens", 0),
        completion_tokens=usage.get("completion_tokens", 0),
        total_tokens=usage.get("total_tokens", 0),
        content_filter_results=content_filter_results,
        resource_region=_extract_azure_region(client),
    )

    return PlatformModelResponse(
        content=content,
        model_id=model_id,
        deployment_name=resolved_deployment,
        request_id=request_id,
        finish_reason=finish_reason,
        usage=usage,
        raw_response=response,
    )


def _extract_azure_region(client: AzureOpenAI) -> Optional[str]:
    """
    Extract the Azure region from the client endpoint URL.

    Azure OpenAI endpoints follow the pattern:
    https://<resource-name>.openai.azure.com/

    The region can be inferred from the resource name or endpoint metadata.

    Args:
        client: AzureOpenAI client instance.

    Returns:
        Azure region string if determinable, otherwise None.
    """
    endpoint = getattr(client, "_base_url", None)
    if endpoint:
        endpoint_str = str(endpoint)
        # Azure endpoints don't directly encode region in URL
        # Return the host as a resource identifier
        if "openai.azure.com" in endpoint_str:
            return endpoint_str
    return None


def collect_metadata_from_existing_response(
    response,
    deployment_name: str,
) -> PlatformMetadata:
    """
    Build a PlatformMetadata object from an existing Azure OpenAI response.

    Useful for post-processing responses that were already captured.

    Args:
        response: Raw Azure OpenAI response object.
        deployment_name: The deployment name used for the request.

    Returns:
        PlatformMetadata populated with provider metadata.
    """
    usage = extract_token_usage(response)
    model_id = getattr(response, "model", deployment_name)
    system_fingerprint = getattr(response, "system_fingerprint", None)
    created_timestamp = getattr(response, "created", None)

    content_filter_results = None
    if response.choices and len(response.choices) > 0:
        choice = response.choices[0]
        if hasattr(choice, "content_filter_results"):
            content_filter_results = choice.content_filter_results

    return PlatformMetadata(
        model_id=model_id,
        deployment_name=deployment_name,
        created_timestamp=created_timestamp,
        system_fingerprint=system_fingerprint,
        prompt_tokens=usage.get("prompt_tokens", 0),
        completion_tokens=usage.get("completion_tokens", 0),
        total_tokens=usage.get("total_tokens", 0),
        content_filter_results=content_filter_results,
    )
