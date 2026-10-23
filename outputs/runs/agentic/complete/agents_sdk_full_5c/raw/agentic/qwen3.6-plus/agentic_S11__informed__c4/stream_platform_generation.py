"""Stream output from a managed model platform while preserving provider response objects.

Streams output from Amazon Bedrock foundation models using the invoke_model_with_response_stream
API. Yields StreamingChunk objects as content arrives while preserving the full
provider response for metadata extraction.

Provider: Amazon Bedrock
SDK: boto3 (bedrock-runtime client)
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

import json
from typing import Generator, List, Optional, Tuple

from model_client import create_bedrock_runtime_client, resolve_bedrock_credentials
from model_models import (
    PlatformModelRequest,
    StreamingChunk,
    parse_bedrock_stream_event,
    normalize_prompt_for_bedrock,
)


def stream_bedrock_generation(
    prompt: str,
    model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0",
    system_prompt: Optional[str] = None,
    max_tokens: int = 2048,
    temperature: float = 0.7,
    top_p: float = 0.9,
    stop_sequences: Optional[List[str]] = None,
) -> Generator[StreamingChunk, None, dict]:
    """Stream tokens from an Amazon Bedrock model invocation.

    Yields StreamingChunk objects as content is generated. The generator
    returns a dict with full provider metadata upon completion.

    Args:
        prompt: User prompt to send to the model.
        model_id: Bedrock model identifier.
        system_prompt: Optional system prompt.
        max_tokens: Maximum tokens to generate.
        temperature: Sampling temperature.
        top_p: Top-p sampling parameter.
        stop_sequences: Optional stop sequences.

    Yields:
        StreamingChunk with text content or metadata.

    Returns:
        Dict with full provider response metadata.

    Raises:
        ValueError: If prompt is empty.
    """
    normalized_prompt = normalize_prompt_for_bedrock(prompt)

    request = PlatformModelRequest(
        prompt=normalized_prompt,
        system_prompt=system_prompt,
        model_id=model_id,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        stop_sequences=stop_sequences,
        stream=True,
    )

    credentials = resolve_bedrock_credentials()
    client = create_bedrock_runtime_client(credentials)

    payload = request.to_bedrock_payload()

    response = client.invoke_model_with_response_stream(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(payload),
    )

    stream = response.get("body")
    full_text = []
    provider_metadata = {}

    if stream is None:
        raise ValueError("Bedrock streaming response body is None")

    for event in stream:
        chunk_bytes = event.get("chunk", {}).get("bytes", b"")
        if not chunk_bytes:
            continue

        try:
            chunk_data = json.loads(chunk_bytes.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue

        parsed = parse_bedrock_stream_event(chunk_data)

        if parsed is None:
            continue

        if parsed.is_final:
            provider_metadata.update(parsed.metadata or {})
            provider_metadata["model_id"] = model_id
            provider_metadata["response_metadata"] = response.get("ResponseMetadata", {})
            continue

        if parsed.text:
            full_text.append(parsed.text)
            yield parsed

    provider_metadata["full_text"] = "".join(full_text)
    provider_metadata["model_id"] = model_id
    return provider_metadata


def stream_to_complete_text(
    prompt: str,
    model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0",
    **kwargs,
) -> Tuple[str, dict]:
    """Stream generation and return complete text with metadata.

    Convenience function that consumes the stream and returns aggregated text
    alongside provider metadata.

    Args:
        prompt: User prompt.
        model_id: Bedrock model identifier.
        **kwargs: Additional streaming parameters.

    Returns:
        Tuple of (complete_text, metadata_dict).
    """
    gen = stream_bedrock_generation(prompt=prompt, model_id=model_id, **kwargs)
    chunks = []
    metadata = None

    for chunk in gen:
        if chunk.text:
            chunks.append(chunk.text)

    try:
        metadata = gen.send(None)
    except StopIteration as e:
        metadata = e.value if e.value else {}

    return "".join(chunks), metadata


if __name__ == "__main__":
    gen = stream_bedrock_generation("Tell me a short story about a robot.")
    for chunk in gen:
        if chunk.text:
            print(chunk.text, end="", flush=True)
