import json
from typing import Iterator
from model_client import get_bedrock_client
from model_models import ModelRequest, StreamChunk
from select_platform_resource import get_bedrock_model_id


def stream_generation(request: ModelRequest) -> Iterator[StreamChunk]:
    """
    Streams the output from a model on Amazon Bedrock.
    """
    client = get_bedrock_client()
    model_id = get_bedrock_model_id("anthropic.claude-instant-v1")

    body = json.dumps(
        {
            "prompt": f"\n\nHuman: {request.prompt}\n\nAssistant:",
            "max_tokens_to_sample": request.max_tokens,
            "temperature": request.temperature,
        }
    )

    response = client.invoke_model_with_response_stream(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json",
    )

    for event in response.get("body"):
        chunk = json.loads(event["chunk"]["bytes"])
        if "completion" in chunk:
            yield StreamChunk(text=chunk["completion"], raw_chunk=chunk)
