import boto3

from model_client import BedrockClient


def translate_result(payload, config=None):
    config = config or {}
    client = BedrockClient(config)
    prompt = "Translate the following text to the target language:\n\n" + payload["text"] + "\n\nTarget Language: " + payload["target_language"]
    response = client.converse(
        modelId="amazon.nova-pro-v1:0",
        messages=[{"role": "user", "content": [{"text": prompt}]}],
    )
    text = "".join(block["text"] for block in response["output"]["message"]["content"] if "text" in block)
    return {"text": text}