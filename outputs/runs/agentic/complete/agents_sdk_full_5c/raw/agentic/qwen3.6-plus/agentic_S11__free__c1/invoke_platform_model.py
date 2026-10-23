"""Invoke a provider-managed model through an OpenAI inference-profile-scoped platform client.

Uses the openai.OpenAI chat.completions.create endpoint to invoke a managed
OpenAI model (e.g., gpt-4o) with a normalized request payload.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from openai import OpenAI
from openai.types.chat import ChatCompletion

from model_client import create_openai_client, with_retry
from model_models import PlatformModelRequest, PlatformModelResponse


def invoke_platform_model(
    request: PlatformModelRequest,
    client: Optional[OpenAI] = None,
) -> PlatformModelResponse:
    """Invoke an OpenAI managed model and return a normalized response.

    Args:
        request: A PlatformModelRequest with resolved OpenAI model_id.
        client: Optional pre-configured OpenAI client instance.

    Returns:
        A PlatformModelResponse carrying the model output and metadata.
    """
    resolved_client = client or create_openai_client()
    payload = request.to_openai_payload()
    payload["stream"] = False

    def _call() -> ChatCompletion:
        return resolved_client.chat.completions.create(**payload)

    completion: ChatCompletion = with_retry(_call)

    return PlatformModelResponse.from_openai_completion(completion)


def invoke_platform_model_raw(
    messages: List[Dict[str, str]],
    model_id: Optional[str] = None,
    temperature: float = 1.0,
    max_tokens: Optional[int] = None,
    client: Optional[OpenAI] = None,
    **extra_kwargs: Any,
) -> PlatformModelResponse:
    """Convenience wrapper: build a request inline and invoke the OpenAI platform.

    Uses OPENAI_API_KEY from the environment and resolves model_id via
    resolve_deployment_model if not provided.
    """
    from model_client import resolve_deployment_model

    effective_model = resolve_deployment_model(model_id)
    request = PlatformModelRequest(
        model_id=effective_model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=False,
    )
    return invoke_platform_model(request, client=client)
