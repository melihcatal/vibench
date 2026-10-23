import boto3


def stream_platform_generation(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region", "us-east-1"))
    response = client.converse_stream(
        modelId=config.get("model_id", "us.amazon.nova-pro-v1:0"),
        messages=[{"role": "user", "content": [{"text": payload["text"]}]}],
    )
    chunks = []
    for event in response.get("stream", []):
        if "contentBlockDelta" in event:
            delta = event["contentBlockDelta"].get("delta", {})
            if "text" in delta:
                chunks.append(delta["text"])
    return {"stream": response, "text": "".join(chunks)}
