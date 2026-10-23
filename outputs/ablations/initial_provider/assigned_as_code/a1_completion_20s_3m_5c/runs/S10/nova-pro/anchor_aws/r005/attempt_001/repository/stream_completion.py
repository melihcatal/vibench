import boto3

from model_client import BedrockClient


def stream_completion(payload, config=None):
    config = config or {}
    client = BedrockClient(config)
    prompt = payload["text"]
    response = client.stream_completion(
        modelId="amazon.nova-pro-v1:0",
        messages=[{"role": "user", "content": [{"text": prompt}]}],
    )
    return response