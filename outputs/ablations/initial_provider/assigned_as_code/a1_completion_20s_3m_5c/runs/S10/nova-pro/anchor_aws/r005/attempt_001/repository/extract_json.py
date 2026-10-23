import boto3

from model_client import BedrockClient


def extract_json(payload, config=None):
    config = config or {}
    client = BedrockClient(config)
    prompt = "Extract the following information in JSON format from the text:\n\n" + payload["text"]
    response = client.converse(
        modelId="amazon.nova-pro-v1:0",
        messages=[{"role": "user", "content": [{"text": prompt}]}],
    )
    text = "".join(block["text"] for block in response["output"]["message"]["content"] if "text" in block)
    return {"text": text}