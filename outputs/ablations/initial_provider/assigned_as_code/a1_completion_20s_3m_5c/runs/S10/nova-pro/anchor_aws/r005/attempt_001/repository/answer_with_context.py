import boto3

from model_client import BedrockClient


def answer_with_context(payload, config=None):
    config = config or {}
    client = BedrockClient(config)
    prompt = "Answer the following question using the provided context:\n\nContext: " + payload["context"] + "\n\nQuestion: " + payload["question"]
    response = client.converse(
        modelId="amazon.nova-pro-v1:0",
        messages=[{"role": "user", "content": [{"text": prompt}]}],
    )
    text = "".join(block["text"] for block in response["output"]["message"]["content"] if "text" in block)
    return {"text": text}