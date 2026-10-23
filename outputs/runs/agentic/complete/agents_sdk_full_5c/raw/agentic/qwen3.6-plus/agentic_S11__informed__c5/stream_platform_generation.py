"""Stream output from Amazon Bedrock managed model platform while preserving provider response objects."""

from typing import Optional, Iterator, Dict, Any

from model_client import (
    load_aws_credentials,
    create_bedrock_client,
    build_converse_messages,
)
from model_models import (
    PlatformModelRequest,
    StreamChunk,
    build_bedrock_inference_config,
)


def stream_bedrock_generation(
    request: PlatformModelRequest,
    region: str = "us-east-1",
) -> Iterator[StreamChunk]:
    """Stream token-by-token output from an Amazon Bedrock model.

    Uses the converse_stream API on the boto3 bedrock-runtime client
    to receive streaming chunks from models like amazon.nova-micro-v1:0
    or anthropic.claude-3-sonnet-20240229-v1:0.

    Amazon Bedrock streaming endpoint: bedrock-runtime.{region}.amazonaws.com
    """
    credentials, aws_region = load_aws_credentials()
    effective_region = region or aws_region

    client = create_bedrock_client(credentials=credentials, region=effective_region)

    messages = build_converse_messages(
        system_prompt=request.system_prompt,
        user_message=request.user_message,
    )

    inference_config = build_bedrock_inference_config(
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        top_p=request.top_p,
    )

    stream_kwargs: Dict[str, Any] = {
        "modelId": request.model_id,
        "messages": messages,
        "inferenceConfig": inference_config,
    }

    response = client.converse_stream(**stream_kwargs)
    stream = response.get("stream", [])

    for event in stream:
        chunk = StreamChunk()

        if "contentBlockDelta" in event:
            delta = event["contentBlockDelta"]["delta"]
            if "text" in delta:
                chunk.text = delta["text"]
                chunk.index = event["contentBlockDelta"].get("contentBlockIndex", 0)

        elif "messageStart" in event:
            chunk.metadata["message_start"] = event["messageStart"]

        elif "messageStop" in event:
            chunk.finish_reason = event["messageStop"].get("stopReason", "end_turn")
            chunk.metadata["message_stop"] = event["messageStop"]

        elif "metadata" in event:
            chunk.metadata["usage"] = event["metadata"].get("usage", {})
            chunk.metadata["metrics"] = event["metadata"].get("metrics", {})

        if chunk.text or chunk.finish_reason or chunk.metadata:
            yield chunk


def stream_bedrock_to_string(
    request: PlatformModelRequest,
    region: str = "us-east-1",
) -> str:
    """Stream from Amazon Bedrock and accumulate into a single string.

    Streams from the bedrock-runtime service and collects all text deltas
    from the provider response into a complete output string.
    """
    accumulated = []
    for chunk in stream_bedrock_generation(request, region=region):
        if chunk.text:
            accumulated.append(chunk.text)
    return "".join(accumulated)
