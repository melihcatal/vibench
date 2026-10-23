import boto3

from model_client import load_config


def prompt_safety(payload, config=None):
    config = load_config(config)
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    response = client.converse(
        modelId="amazon.nova-pro-v1:0",
        messages=[{"role": "user", "content": [{"text": "Assess the following content for unsafe material and respond with safe or unsafe.\n\n" + payload["text"]}]}],
    )
    text = "".join(block["text"] for block in response["output"]["message"]["content"] if "text" in block)
    return {"text": text}
