from model_client import create_openai_client, OPENAI_API_BASE
from model_models import PlatformModelRequest, PlatformModelResponse


def collect_platform_metadata(
    messages: list[dict[str, str]],
    model: str = "gpt-4o",
    temperature: float = 0.7,
    max_tokens: int | None = None,
    **kwargs,
) -> dict:
    client = create_openai_client(base_url=OPENAI_API_BASE)
    request = PlatformModelRequest(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        **kwargs,
    )
    payload = request.to_openai_payload()
    response = client.chat.completions.create(**payload)
    normalized = PlatformModelResponse.from_openai_response(response)

    metadata = {
        "content": normalized.content,
        "model": normalized.model,
        "finish_reason": normalized.finish_reason,
        "request_id": normalized.request_id,
        "system_fingerprint": normalized.system_fingerprint,
        "created": normalized.created,
        "provider": "openai",
        "api_endpoint": OPENAI_API_BASE,
    }

    if normalized.usage:
        metadata["usage"] = {
            "prompt_tokens": normalized.usage.prompt_tokens,
            "completion_tokens": normalized.usage.completion_tokens,
            "total_tokens": normalized.usage.total_tokens,
        }
        if normalized.usage.completion_tokens_details:
            metadata["usage"]["completion_tokens_details"] = (
                normalized.usage.completion_tokens_details
            )

    return metadata
