import boto3


def collect_platform_metadata(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region", "us-east-1"))
    response = client.converse(
        modelId=config.get("model_id", "us.amazon.nova-pro-v1:0"),
        messages=[{"role": "user", "content": [{"text": payload["text"]}]}],
    )
    content = response["output"]["message"]["content"]
    text = "".join(block.get("text", "") for block in content)
    return {
        "text": text,
        "usage": response.get("usage", {}),
        "model_id": response.get("modelId", config.get("model_id", "us.amazon.nova-pro-v1:0")),
        "request_id": response.get("ResponseMetadata", {}).get("RequestId"),
    }
