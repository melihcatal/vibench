import boto3

from model_client import BedrockClient


def generate_spoken_brief(payload, config=None):
    config = config or {}
    client = BedrockClient(config)
    prompt = "Generate a spoken brief from the following text:\n\n" + payload["text"]
    response = client.converse(
        modelId="amazon.nova-pro-v1:0",
        messages=[{"role": "user", "content": [{"text": prompt}]}],
    )
    text = "".join(block["text"] for block in response["output"]["message"]["content"] if "text" in block)
    return {"text": text}