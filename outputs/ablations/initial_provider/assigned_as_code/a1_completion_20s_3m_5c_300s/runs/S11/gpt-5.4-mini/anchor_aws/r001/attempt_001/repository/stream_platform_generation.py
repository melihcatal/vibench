import boto3

from model_client import get_runtime_client


def stream_platform_generation(payload, config=None):
    config = config or {}
    client = get_runtime_client(config)
    response = client.converse_stream(
        modelId=config.get("model_id", "us.amazon.nova-pro-v1:0"),
        messages=[{"role": "user", "content": [{"text": payload["text"]}]],
    )
    chunks = []
    for event in response["stream"]:
        if "contentBlockDelta" in event and "text" in event["contentBlockDelta"].get("delta", {}):
            chunks.append(event["contentBlockDelta"]["delta"]["text"])
    return {"stream": response, "text": "".join(chunks)}
