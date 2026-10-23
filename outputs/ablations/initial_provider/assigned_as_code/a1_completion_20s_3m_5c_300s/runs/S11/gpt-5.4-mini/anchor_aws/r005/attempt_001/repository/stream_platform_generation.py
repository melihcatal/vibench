import boto3

from model_client import get_region


def stream_platform_generation(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=get_region(config))
    response = client.converse_stream(
        modelId=config.get("model_id", "us.amazon.nova-pro-v1:0"),
        messages=[{"role": "user", "content": [{"text": payload["text"]}]}],
    )
    chunks = []
    for event in response["stream"]:
        if "contentBlockDelta" in event and "text" in event["contentBlockDelta"].get("delta", {}):
            chunks.append(event["contentBlockDelta"]["delta"]["text"])
    return {"text": "".join(chunks), "response": response}
