"""Collect model output together with OpenAI platform metadata."""

from openai import OpenAI

from model_client import get_openai_client, PLATFORM_MODEL_DEFAULT
from model_models import PlatformRequest, PlatformResponse, PlatformMetadata


def collect_platform_metadata(
    prompt: str,
    model: str | None = None,
    temperature: float = 0.7,
    max_tokens: int = 1024,
) -> tuple[PlatformResponse, PlatformMetadata]:
    """Invoke the OpenAI model and return output plus platform metadata.

    Metadata includes token usage, model ID, system fingerprint, and
    resource identifiers returned by api.openai.com for the gpt-4o
    model family.
    """
    model_id = model or PLATFORM_MODEL_DEFAULT
    client = get_openai_client()

    request = PlatformRequest(
        prompt=prompt,
        model=model_id,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    response = client.chat.completions.create(
        model=request.model,
        messages=[{"role": "user", "content": request.prompt}],
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )

    raw_text = response.choices[0].message.content or ""
    finish_reason = response.choices[0].finish_reason

    usage = response.usage
    metadata = PlatformMetadata(
        model_id=response.model,
        prompt_tokens=usage.prompt_tokens if usage else 0,
        completion_tokens=usage.completion_tokens if usage else 0,
        total_tokens=usage.total_tokens if usage else 0,
        system_fingerprint=response.system_fingerprint,
        response_id=response.id,
        created=response.created,
    )

    platform_response = PlatformResponse(
        text=raw_text,
        finish_reason=finish_reason,
        model=response.model,
        raw_response=response,
    )

    return platform_response, metadata


if __name__ == "__main__":
    resp, meta = collect_platform_metadata("What is the capital of France?")
    print(f"Answer: {resp.text}")
    print(f"Tokens used: {meta.total_tokens}")
    print(f"Model: {meta.model_id}")
    print(f"Response ID: {meta.response_id}")
