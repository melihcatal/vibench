import boto3


def stream_platform_generation(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region", "us-east-1"))
    response = client.converse(
        modelId="us.amazon.nova-pro-v1:0",
        messages=[{"role": "user", "content": [{"text": payload["text"]}]}],
    )
    for block in response["output"]["message"]["content"]:
        if "text" in block:
            yield block["text"]