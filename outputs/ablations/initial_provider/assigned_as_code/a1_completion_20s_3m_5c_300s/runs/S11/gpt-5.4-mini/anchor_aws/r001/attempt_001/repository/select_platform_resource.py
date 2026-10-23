import boto3

from model_client import get_region, get_runtime_client


def select_platform_resource(payload, config=None):
    config = config or {}
    client = get_runtime_client(config)
    response = client.converse(
        modelId=config.get("model_id", "us.amazon.nova-pro-v1:0"),
        messages=[{"role": "user", "content": [{"text": payload["text"]}]],
    )
    text = "".join(block["text"] for block in response["output"]["message"]["content"] if "text" in block)
    return {"resource_id": response.get("ResponseMetadata", {}).get("RequestId"), "text": text, "region": get_region(config)}
