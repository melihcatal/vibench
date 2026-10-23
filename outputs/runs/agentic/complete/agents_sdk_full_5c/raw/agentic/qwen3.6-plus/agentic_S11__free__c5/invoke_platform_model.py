"""
[SAME-SCENARIO] Invokes a provider-managed model through a project-, deployment-,
or inference-profile-scoped platform client on Azure OpenAI.

Uses the AzureOpenAI SDK client with deployment-scoped invocations to generate
chat completions from Azure OpenAI managed models.
"""

from __future__ import annotations

from typing import Optional

from openai import AzureOpenAI

from model_models import PlatformModelRequest, PlatformModelResponse
from model_client import (
    get_azure_openai_client,
    build_messages,
    extract_text_from_completion,
    extract_token_usage,
)
from select_platform_resource import resolve_deployment_for_request


def invoke_platform_model(
    request: PlatformModelRequest,
    client: Optional[AzureOpenAI] = None,
) -> PlatformModelResponse:
    """
    Invoke an Azure OpenAI managed model via deployment-scoped platform client.

    Sends a chat completion request to the Azure OpenAI service using the
    specified deployment and returns a wrapped response with content and metadata.

    Args:
        request: PlatformModelRequest containing deployment name, messages,
                 and generation parameters.
        client: Optional pre-configured AzureOpenAI client. If not provided,
                a client is created from environment configuration.

    Returns:
        PlatformModelResponse with generated content and response metadata.

    Raises:
        ValueError: If required configuration is missing.
        Exception: If the Azure OpenAI API call fails.
    """
    if client is None:
        client = get_azure_openai_client()

    resolved_deployment, model_config = resolve_deployment_for_request(request, client)

    messages = build_messages(request.system_prompt, request.user_content)

    invocation_params: dict = {
        "model": resolved_deployment,
        "messages": messages,
        "temperature": request.temperature,
        "top_p": request.top_p,
    }

    if request.max_tokens is not None:
        invocation_params["max_tokens"] = request.max_tokens

    if request.stop is not None:
        invocation_params["stop"] = request.stop

    if request.extra_body is not None:
        invocation_params["extra_body"] = request.extra_body

    response = client.chat.completions.create(**invocation_params)

    content = extract_text_from_completion(response)
    usage = extract_token_usage(response)

    model_id = getattr(response, "model", resolved_deployment)
    request_id = getattr(response, "id", None)

    finish_reason = None
    if response.choices and len(response.choices) > 0:
        finish_reason = response.choices[0].finish_reason

    return PlatformModelResponse(
        content=content,
        model_id=model_id,
        deployment_name=resolved_deployment,
        request_id=request_id,
        finish_reason=finish_reason,
        usage=usage,
        raw_response=response,
    )


def invoke_with_retry(
    request: PlatformModelRequest,
    max_retries: int = 3,
    client: Optional[AzureOpenAI] = None,
) -> PlatformModelResponse:
    """
    Invoke an Azure OpenAI managed model with automatic retry on transient errors.

    Retries on rate limit (429) and server error (5xx) responses from
    the Azure OpenAI service.

    Args:
        request: PlatformModelRequest with invocation parameters.
        max_retries: Maximum number of retry attempts.
        client: Optional pre-configured AzureOpenAI client.

    Returns:
        PlatformModelResponse from the successful invocation.

    Raises:
        Exception: If all retry attempts are exhausted.
    """
    import time

    last_exception = None

    for attempt in range(max_retries):
        try:
            return invoke_platform_model(request, client)
        except Exception as e:
            last_exception = e
            error_str = str(e)
            # Retry on Azure OpenAI rate limit or server errors
            if "429" in error_str or "5" in error_str:
                wait_time = min(2 ** attempt * 1.0, 30.0)
                time.sleep(wait_time)
            else:
                raise

    raise last_exception


def invoke_batch(
    requests: list[PlatformModelRequest],
    client: Optional[AzureOpenAI] = None,
) -> list[PlatformModelResponse]:
    """
    Invoke Azure OpenAI managed model for multiple requests sequentially.

    Processes each request through the deployment-scoped Azure OpenAI client.

    Args:
        requests: List of PlatformModelRequest to process.
        client: Optional pre-configured AzureOpenAI client.

    Returns:
        List of PlatformModelResponse objects in the same order as requests.
    """
    results = []
    for req in requests:
        result = invoke_platform_model(req, client)
        results.append(result)
    return results
