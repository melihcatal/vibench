"""Stream output from Amazon Bedrock while preserving provider response objects.

Uses boto3 bedrock-runtime invoke_model_with_response_stream to yield
chunks from anthropic.claude-3-sonnet-20240229-v1:0 on Amazon Bedrock.
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

import json
from typing import Dict, Generator, Optional

from model_client import get_bedrock_runtime_client
from model_models import PlatformModelRequest, StreamChunk

BEDROCK_MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"


def stream_platform_generation(
    prompt: str,
    model_id: str = BEDROCK_MODEL_ID,
    system_prompt: str = "",
    max_tokens: int = 1024,
    temperature: float = 0.7,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
) -> Generator[StreamChunk, None, None]:
    """Stream generation from an Amazon Bedrock model.

    Uses the bedrock-runtime invoke_model_with_response_stream API
    to receive token-by-token deltas from anthropic.claude-3-sonnet-20240229-v1:0.
    Yields StreamChunk objects containing text deltas and raw provider events.
    """
    request = PlatformModelRequest.from_text(
        text=prompt,
        model_id=model_id,
        system_prompt=system_prompt,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    client = get_bedrock_runtime_client(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    body_bytes = request.to_bedrock_payload()

    response = client.invoke_model_with_response_stream(
        modelId=request.model_id,
        body=body_bytes,
        contentType="application/json",
        accept="application/json",
    )

    event_stream = response.get("body")

    if event_stream is None:
        raise RuntimeError("No event stream returned from Bedrock")

    accumulated_text = ""

    for event in event_stream:
        chunk = event.get("chunk", {})
        bytes_data = chunk.get("bytes")
        if bytes_data is None:
            continue

        payload = json.loads(bytes_data.decode("utf-8"))

        if payload.get("type") == "content_block_delta":
            delta = payload.get("delta", {})
            text_delta = delta.get("text", "")
            accumulated_text += text_delta
            yield StreamChunk(
                text=text_delta,
                delta_json=payload,
                is_complete=False,
            )
        elif payload.get("type") == "message_delta":
            delta_info = payload.get("delta", {})
            stop_reason = delta_info.get("stop_reason", "unknown")
            yield StreamChunk(
                text="",
                delta_json=payload,
                is_complete=True,
            )


def collect_streamed_text(
    prompt: str,
    model_id: str = BEDROCK_MODEL_ID,
    system_prompt: str = "",
    max_tokens: int = 1024,
    temperature: float = 0.7,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
) -> str:
    """Helper to collect full streamed output into a single string."""
    chunks: list = []
    for chunk in stream_platform_generation(
        prompt=prompt,
        model_id=model_id,
        system_prompt=system_prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    ):
        chunks.append(chunk.text)
    return "".join(chunks)


if __name__ == "__main__":
    for chunk in stream_platform_generation(
        prompt="Write a haiku about cloud computing.",
        max_tokens=128,
        temperature=0.8,
    ):
        if chunk.text:
            print(chunk.text, end="", flush=True)
        if chunk.is_complete:
            print()
            print("\n[Stream complete]")
