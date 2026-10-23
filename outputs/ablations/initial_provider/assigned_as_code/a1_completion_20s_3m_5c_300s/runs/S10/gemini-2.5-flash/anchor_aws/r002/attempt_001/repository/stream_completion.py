import boto3


def stream_completion(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    prompt = payload["text"]
    response = client.converse_stream(
        modelId="amazon.nova-pro-v1:0",
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"temperature": 0.9, "maxTokens": 2048},
    )

    for chunk in response["stream"]:
        if "contentBlockDelta" in chunk and "text" in chunk["contentBlockDelta"]:
            yield {"token": chunk["contentBlockDelta"]["text"]}
