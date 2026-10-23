import os
import json
import boto3
from botocore.exceptions import ClientError
from model_client import get_bedrock_runtime_client
from model_models import InvocationRequest, StreamingChunk
from typing import Generator

def stream_platform_generation(request: InvocationRequest) -> Generator[StreamingChunk, None, None]:
    """Streams output from a managed model platform while preserving provider response objects."""
    bedrock_runtime_client = get_bedrock_runtime_client()

    # Construct the body for the Anthropic Claude model
    body = json.dumps({
        "messages": [{
            "role": "user",
            "content": request.prompt
        }],
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": request.max_tokens or 1000,
        "temperature": request.temperature or 0.7
    })

    try:
        response = bedrock_runtime_client.invoke_model_with_response_stream(
            body=body,
            modelId=request.model_id or "anthropic.claude-3-haiku-20240307-v1:0",
            accept="application/json",
            contentType="application/json"
        )

        stream = response.get("body")
        for event in stream:
            if "chunk" in event:
                chunk = event.get("chunk")
                bytes_payload = chunk.get("bytes")
                if bytes_payload:
                    payload = json.loads(bytes_payload.decode('utf-8'))
                    # Handle different types of events in Claude 3 stream
                    if payload.get("type") == "content_block_delta":
                        text = payload.get("delta", {}).get("text", "")
                        yield StreamingChunk(text_content=text, raw_event=payload)
                    elif payload.get("type") == "message_stop":
                        yield StreamingChunk(text_content="", raw_event=payload, is_end=True)
                    elif payload.get("type") == "message_start":
                        yield StreamingChunk(text_content="", raw_event=payload, is_start=True)
                    elif payload.get("type") == "message_delta":
                         # Handle usage for the full message
                         usage = payload.get("usage", {})
                         yield StreamingChunk(text_content="", raw_event=payload, input_token_count=usage.get("input_tokens"), output_token_count=usage.get("output_tokens"))

    except ClientError as e:
        raise RuntimeError(f"Bedrock streaming model invocation failed: {e}")
