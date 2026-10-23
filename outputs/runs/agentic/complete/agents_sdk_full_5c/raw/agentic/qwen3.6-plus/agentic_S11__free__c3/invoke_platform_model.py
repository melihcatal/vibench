"""Invokes a provider-managed model through a project-scoped OpenAI platform client.

Uses the OpenAI Chat Completions API with the gpt-4o-2024-08-06 model
to generate responses through the project-scoped platform client.
"""

from typing import Dict, Any, Optional

from model_client import load_platform_config, get_openai_client, extract_text_from_completion
from model_models import (
    PlatformInvocationRequest,
    PlatformInvocationResponse,
    build_platform_request,
)


OPENAI_PLATFORM_MODEL = "gpt-4o-2024-08-06"


def invoke_platform_model(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
    provider_config: Optional[Dict[str, Any]] = None,
) -> PlatformInvocationResponse:
    """Invoke the OpenAI managed model platform through a project-scoped client.

    This function uses the OpenAI SDK client to invoke the gpt-4o model
    via the project-scoped Chat Completions endpoint, returning a normalized
    response with text, model identifier, usage, and response ID.

    Args:
        prompt: User input text to send to the model.
        system_prompt: Optional system-level instructions.
        model: Override the default OpenAI model identifier.
        temperature: Sampling temperature (0.0 to 2.0).
        max_tokens: Maximum tokens to generate.
        provider_config: Optional pre-loaded provider configuration.

    Returns:
        PlatformInvocationResponse with generated text and metadata.
    """
    if provider_config is None:
        provider_config = load_platform_config("openai")

    model_id = model or provider_config.get("default_model", OPENAI_PLATFORM_MODEL)

    client = get_openai_client(provider_config)

    request = build_platform_request(
        prompt=prompt,
        system_prompt=system_prompt,
        model=model_id,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    messages = request.to_openai_messages()

    completion = client.chat.completions.create(
        model=model_id,
        messages=messages,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        top_p=request.top_p,
    )

    text = extract_text_from_completion(completion)

    usage = None
    if hasattr(completion, "usage"):
        usage = {
            "prompt_tokens": completion.usage.prompt_tokens,
            "completion_tokens": completion.usage.completion_tokens,
            "total_tokens": completion.usage.total_tokens,
        }

    response_id = getattr(completion, "id", None)
    response_model = getattr(completion, "model", model_id)

    return PlatformInvocationResponse(
        text=text,
        model=response_model,
        response_id=response_id,
        usage=usage,
        raw_response=completion,
        provider="openai",
    )


def invoke_with_extra_params(
    prompt: str,
    extra_params: Optional[Dict[str, Any]] = None,
    provider_config: Optional[Dict[str, Any]] = None,
) -> PlatformInvocationResponse:
    """Invoke the platform model with provider-specific extra parameters.

    Supports OpenAI-specific parameters like response_format, tools,
    and function calling through the project-scoped client.

    Args:
        prompt: User input text.
        extra_params: OpenAI-specific parameters (e.g., response_format, tools).
        provider_config: Optional pre-loaded configuration.

    Returns:
        PlatformInvocationResponse with generated text.
    """
    if provider_config is None:
        provider_config = load_platform_config("openai")

    model_id = provider_config.get("default_model", OPENAI_PLATFORM_MODEL)
    client = get_openai_client(provider_config)

    messages = [
        {"role": "user", "content": prompt},
    ]

    create_kwargs: Dict[str, Any] = {
        "model": model_id,
        "messages": messages,
    }

    if extra_params:
        create_kwargs.update(extra_params)

    completion = client.chat.completions.create(**create_kwargs)

    text = extract_text_from_completion(completion)

    return PlatformInvocationResponse(
        text=text,
        model=model_id,
        response_id=getattr(completion, "id", None),
        raw_response=completion,
        provider="openai",
    )
