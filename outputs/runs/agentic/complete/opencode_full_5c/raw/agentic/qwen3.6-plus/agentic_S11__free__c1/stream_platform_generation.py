from typing import Optional

from model_client import get_bedrock_runtime_client, resolve_model_resource
from model_models import (
    PlatformModelRequest,
    PlatformStreamResponse,
    StreamChunk,
    build_bedrock_converse_payload,
    normalize_bedrock_stream_usage,
)


BEDROCK_DEFAULT_MODEL = "anthropic.claude-3-sonnet-20240229-v1:0"


def stream_platform_generation(
    prompt: str,
    model_id: Optional[str] = None,
    system_prompt: Optional[str] = None,
    max_tokens: int = 1024,
    temperature: float = 0.7,
    top_p: float = 0.9,
    stop_sequences: Optional[list[str]] = None,
    inference_profile_arn: Optional[str] = None,
    region: Optional[str] = None,
) -> PlatformStreamResponse:
    resource = resolve_model_resource(model_id or BEDROCK_DEFAULT_MODEL)
    target_model_id = resource.model_id
    if inference_profile_arn:
        target_model_id = inference_profile_arn

    client = get_bedrock_runtime_client(region=region)

    request = PlatformModelRequest(
        model_id=target_model_id,
        prompt=prompt,
        system_prompt=system_prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        stop_sequences=stop_sequences,
        inference_profile_arn=inference_profile_arn,
    )

    payload = build_bedrock_converse_payload(request)

    stream_response = client.converse_stream(**payload)
    event_stream = stream_response.get("stream")

    chunks: list[StreamChunk] = []
    full_text = ""
    chunk_index = 0
    stop_reason = ""
    input_tokens = 0
    output_tokens = 0
    total_tokens = 0
    request_id = stream_response.get("ResponseMetadata", {}).get("RequestId")

    for event in event_stream:
        if "contentBlockDelta" in event:
            delta = event["contentBlockDelta"].get("delta", {})
            text = delta.get("text", "")
            if text:
                full_text += text
                chunk = StreamChunk(
                    text=text,
                    index=chunk_index,
                    is_final=False,
                    raw_chunk=event["contentBlockDelta"],
                )
                chunks.append(chunk)
                chunk_index += 1

        elif "contentBlockStop" in event:
            pass

        elif "messageStop" in event:
            stop_reason = event["messageStop"].get("stopReason", "end_turn")

        elif "metadata" in event:
            usage = event["metadata"].get("usage", {})
            token_info = normalize_bedrock_stream_usage(usage)
            input_tokens = token_info["input_tokens"]
            output_tokens = token_info["output_tokens"]
            total_tokens = token_info["total_tokens"]

    if chunks:
        chunks[-1].is_final = True

    return PlatformStreamResponse(
        chunks=chunks,
        model_id=resource.model_id,
        stop_reason=stop_reason,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
        request_id=request_id,
        resource_arn=resource.model_arn,
    )
