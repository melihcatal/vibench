import boto3


def result_translate(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    prompt = f'Translate the following text to {payload["target_language"]}:\n\n{payload["text"]}'
    response = client.converse(
        modelId=config.get("model_id", "amazon.nova-pro-v1:0"),
        messages=[{"role": "user", "content": [{"text": prompt}]}],
    )
    text = "".join(block["text"] for block in response["output"]["message"]["content"] if "text" in block)
    return {"text": text}
