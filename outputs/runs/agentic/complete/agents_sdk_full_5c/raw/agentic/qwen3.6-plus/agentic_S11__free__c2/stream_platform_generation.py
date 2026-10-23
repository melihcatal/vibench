"""Stream output from an OpenAI managed model platform via streaming API."""

from openai import OpenAI
from openai.types.chat import ChatCompletionChunk

from model_client import get_openai_client, PLATFORM_MODEL_DEFAULT
from model_models import PlatformRequest, PlatformResponse


def stream_platform_generation(
    prompt: str,
    model: str | None = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
) -> list[ChatCompletionChunk]:
    """Stream tokens from the OpenAI platform and preserve raw ChatCompletionChunk objects.

    Connects to api.openai.com using the OpenAI SDK streaming endpoint
    so every chunk is a provider-native ChatCompletionChunk from the
    gpt-4o model family.
    """
    model_id = model or PLATFORM_MODEL_DEFAULT
    client = get_openai_client()

    request = PlatformRequest(
        prompt=prompt,
        model=model_id,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    stream = client.chat.completions.create(
        model=request.model,
        messages=[{"role": "user", "content": request.prompt}],
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        stream=True,
    )

    chunks: list[ChatCompletionChunk] = []
    for chunk in stream:
        chunks.append(chunk)
        delta = chunk.choices[0].delta if chunk.choices else None
        if delta and delta.content:
            print(delta.content, end="", flush=True)

    print()
    return chunks


def build_response_from_stream(chunks: list[ChatCompletionChunk], model_id: str) -> PlatformResponse:
    """Reconstruct a PlatformResponse from streamed OpenAI chunks."""
    full_text = ""
    finish_reason = None
    for chunk in chunks:
        if chunk.choices:
            choice = chunk.choices[0]
            if choice.delta and choice.delta.content:
                full_text += choice.delta.content
            if choice.finish_reason:
                finish_reason = choice.finish_reason

    return PlatformResponse(
        text=full_text,
        finish_reason=finish_reason,
        model=model_id,
        raw_response=chunks[-1] if chunks else None,
    )


if __name__ == "__main__":
    result_chunks = stream_platform_generation("Write a haiku about cloud computing.")
    response = build_response_from_stream(result_chunks, PLATFORM_MODEL_DEFAULT)
    print(f"\nFinal text ({len(response.text)} chars): {response.text}")
