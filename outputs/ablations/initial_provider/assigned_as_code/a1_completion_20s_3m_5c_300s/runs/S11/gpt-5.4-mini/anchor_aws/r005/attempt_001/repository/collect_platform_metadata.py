import boto3

from model_client import get_region


def collect_platform_metadata(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=get_region(config))
    response = client.converse(
        modelId=config.get("model_id", "us.amazon.nova-pro-v1:0"),
        messages=[{"role": "user", "content": [{"text": payload["text"]}]}],
    )
    text = "".join(block["text"] for block in response["output"]["message"]["content"] if "text" in block)
    usage = response.get("usage", {})
    return {"text": text, "usage": usage, "model_id": response.get("modelId", config.get("model_id", "us.amazon.nova-pro-v1:0")), "response": response}
