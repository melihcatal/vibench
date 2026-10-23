"""Stream output from an Azure OpenAI managed model while preserving provider response objects.

Uses Azure OpenAI Service (sdk=openai) with AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY.
"""

from typing import Iterator, Optional, Generator

from openai import AzureOpenAI
from openai.types.chat import ChatCompletionChunk

from model_client import create_azure_openai_client, get_default_deployment
from model_models import ModelRequest, PlatformMetadata, ModelResponse, build_streaming_chunks


def stream_platform_generation(
    prompt: str,
    system_prompt: Optional[str] = None,
    deployment: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
    client: Optional[AzureOpenAI] = None,
) -> Generator[ChatCompletionChunk, None, ModelResponse]:
    """Stream text from Azure OpenAI and yield each ChatCompletionChunk.

    Yields each ChatCompletionChunk as it arrives, and after the stream
    is exhausted, returns a fully assembled ModelResponse via the generator's
    return value.

    Args:
        prompt: User input text.
        system_prompt: Optional system-level instruction.
        deployment: Azure OpenAI deployment name.
        temperature: Sampling temperature.
        max_tokens: Maximum completion tokens.
        client: Optional pre-configured AzureOpenAI client.

    Yields:
        ChatCompletionChunk objects from the Azure OpenAI streaming API.

    Returns:
        Final ModelResponse with assembled text and provider metadata.
    """
    resolved_client = client or create_azure_openai_client()
    resolved_deployment = deployment or get_default_deployment()

    request = ModelRequest(
        prompt=prompt,
        deployment=resolved_deployment,
        temperature=temperature,
        max_tokens=max_tokens,
        system_prompt=system_prompt,
        stream=True,
    )

    messages = request.to_openai_messages()

    raw_stream = resolved_client.chat.completions.create(
        model=resolved_deployment,
        messages=messages,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        top_p=request.top_p,
        stream=True,
    )

    text_chunks: list[str] = []
    final_chunk: Optional[ChatCompletionChunk] = None
    raw_response_id = ""
    model_name = resolved_deployment
    finish_reason = ""

    for chunk in raw_stream:
        raw_response_id = chunk.id or raw_response_id
        model_name = chunk.model or model_name
        if chunk.choices:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                text_chunks.append(delta.content)
            if chunk.choices[0].finish_reason:
                finish_reason = chunk.choices[0].finish_reason
        final_chunk = chunk
        yield chunk

    full_text = "".join(text_chunks)

    # Build platform metadata from the last chunk and accumulated data
    metadata = PlatformMetadata(
        model=model_name,
        usage_prompt_tokens=0,
        usage_completion_tokens=0,
        usage_total_tokens=0,
        request_id=raw_response_id,
        raw_response=final_chunk,
    )

    # Attempt to extract usage from final chunk if available
    if final_chunk and hasattr(final_chunk, "usage") and final_chunk.usage:
        metadata.usage_prompt_tokens = final_chunk.usage.prompt_tokens
        metadata.usage_completion_tokens = final_chunk.usage.completion_tokens
        metadata.usage_total_tokens = final_chunk.usage.total_tokens

    return ModelResponse(
        text=full_text,
        finish_reason=finish_reason,
        metadata=metadata,
    )


def stream_platform_generation_collect(
    prompt: str,
    system_prompt: Optional[str] = None,
    deployment: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
    client: Optional[AzureOpenAI] = None,
) -> ModelResponse:
    """Convenience wrapper that collects all streamed chunks and returns the final response."""
    gen = stream_platform_generation(
        prompt=prompt,
        system_prompt=system_prompt,
        deployment=deployment,
        temperature=temperature,
        max_tokens=max_tokens,
        client=client,
    )

    chunks = []
    response = None
    for chunk in gen:
        chunks.append(chunk)
        response = chunk

    full_text = "".join(
        c.choices[0].delta.content
        for c in chunks
        if c.choices and c.choices[0].delta and c.choices[0].delta.content
    )

    finish_reason = ""
    if chunks and chunks[-1].choices:
        finish_reason = chunks[-1].choices[0].finish_reason or ""

    return ModelResponse(
        text=full_text,
        finish_reason=finish_reason,
        metadata=PlatformMetadata(
            model=chunks[-1].model if chunks else "",
            request_id=chunks[-1].id if chunks else "",
            raw_response=chunks[-1] if chunks else None,
        ),
    )


if __name__ == "__main__":
    gen = stream_platform_generation(
        prompt="Count from 1 to 5, one per line.",
        system_prompt="You are a concise assistant.",
    )
    for chunk in gen:
        if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print()
