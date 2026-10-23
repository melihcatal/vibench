import boto3

from model_client import get_runtime_client


def collect_platform_metadata(payload, config=None):
    config = config or {}
    client = get_runtime_client(config)
    response = client.converse(
        modelId=config.get("model_id", "us.amazon.nova-pro-v1:0"),
        messages=[{"role": "user", "content": [{"text": payload["text"]}]],
    )
    text = "".join(block["text"] for block in response["output"]["message"]["content"] if "text" in block)
    usage = response.get("usage", {})
    metadata = response.get("ResponseMetadata", {})
    return {"text": text, "usage": usage, "request_id": metadata.get("RequestId"), "model_id": config.get("model_id", "us.amazon.nova-pro-v1:0")}
