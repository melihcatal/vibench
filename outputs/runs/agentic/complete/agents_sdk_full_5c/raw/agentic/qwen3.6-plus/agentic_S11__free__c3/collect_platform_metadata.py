"""Returns model output together with OpenAI provider platform metadata.

Collects and returns the generated text alongside comprehensive
provider platform metadata including usage statistics, response IDs,
model handles, and timing information from the OpenAI platform.
"""

from typing import Dict, Any, Optional

from model_client import load_platform_config, get_openai_client, extract_text_from_completion
from model_models import PlatformMetadata, PlatformInvocationRequest, build_platform_request


OPENAI_METADATA_MODEL = "gpt-4o-2024-08-06"


def collect_platform_metadata(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
    provider_config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Invoke the OpenAI platform and return output with full metadata.

    Generates a response using the OpenAI Chat Completions API and
    collects all available provider platform metadata including token
    usage, response ID, model identifier, and system fingerprint.

    Args:
        prompt: User input text.
        system_prompt: Optional system-level instructions.
        model: Override the default OpenAI model.
        temperature: Sampling temperature.
        max_tokens: Maximum tokens to generate.
        provider_config: Optional pre-loaded configuration.

    Returns:
        Dictionary containing text output and platform metadata.
    """
    if provider_config is None:
        provider_config = load_platform_config("openai")

    model_id = model or provider_config.get("default_model", OPENAI_METADATA_MODEL)
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

    metadata = extract_openai_metadata(completion, model_id)

    return {
        "text": text,
        "metadata": metadata,
        "provider": "openai",
        "model": model_id,
    }


def extract_openai_metadata(
    completion: Any, model_id: str
) -> PlatformMetadata:
    """Extract OpenAI platform metadata from a completion response.

    Parses the OpenAI ChatCompletion response object and builds a
    PlatformMetadata instance with all available fields.

    Args:
        completion: Raw OpenAI ChatCompletion response.
        model_id: The model identifier used for the request.

    Returns:
        PlatformMetadata with collected provider metadata.
    """
    usage_dict = None
    if hasattr(completion, "usage"):
        usage_dict = {
            "prompt_tokens": completion.usage.prompt_tokens,
            "completion_tokens": completion.usage.completion_tokens,
            "total_tokens": completion.usage.total_tokens,
        }

    finish_reason = None
    if completion.choices:
        finish_reason = completion.choices[0].finish_reason

    metadata = PlatformMetadata(
        response_id=getattr(completion, "id", None),
        model_id=getattr(completion, "model", model_id),
        usage=usage_dict,
        finish_reason=finish_reason,
        created_at=getattr(completion, "created", None),
        provider="openai",
        raw_metadata={
            "id": getattr(completion, "id", None),
            "object": getattr(completion, "object", None),
            "created": getattr(completion, "created", None),
            "model": getattr(completion, "model", model_id),
            "system_fingerprint": getattr(completion, "system_fingerprint", None),
            "service_tier": getattr(completion, "service_tier", None),
        },
    )

    return metadata


def get_usage_summary(
    prompt: str,
    model: Optional[str] = None,
    provider_config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Get a usage summary for a platform invocation without returning text.

    Useful for cost estimation and monitoring by capturing only the
    usage metadata from an OpenAI platform invocation.

    Args:
        prompt: User input text.
        model: Model identifier override.
        provider_config: Optional pre-loaded configuration.

    Returns:
        Dictionary with usage-only metadata.
    """
    if provider_config is None:
        provider_config = load_platform_config("openai")

    model_id = model or provider_config.get("default_model", OPENAI_METADATA_MODEL)
    client = get_openai_client(provider_config)

    messages = [{"role": "user", "content": prompt}]

    completion = client.chat.completions.create(
        model=model_id,
        messages=messages,
        max_tokens=1,
        temperature=1.0,
    )

    metadata = extract_openai_metadata(completion, model_id)

    return {
        "model": metadata.model_id,
        "response_id": metadata.response_id,
        "usage": metadata.usage,
        "provider": "openai",
    }


def collect_batch_metadata(
    prompts: list,
    model: Optional[str] = None,
    provider_config: Optional[Dict[str, Any]] = None,
) -> list:
    """Collect metadata from multiple platform invocations.

    Args:
        prompts: List of user prompts to process.
        model: Model identifier override.
        provider_config: Optional pre-loaded configuration.

    Returns:
        List of dictionaries with text and metadata for each prompt.
    """
    results = []
    for p in prompts:
        result = collect_platform_metadata(
            prompt=p,
            model=model,
            provider_config=provider_config,
        )
        results.append(result)
    return results
