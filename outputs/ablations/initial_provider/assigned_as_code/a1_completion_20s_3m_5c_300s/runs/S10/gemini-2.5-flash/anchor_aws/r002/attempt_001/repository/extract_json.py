import boto3


def extract_json(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    prompt = "Extract JSON from the following text:\n\n" + payload["text"]
    response = client.converse(
        modelId="amazon.nova-pro-v1:0",
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"temperature": 0.1, "maxTokens": 2048},
    )
    text = "".join(block["text"] for block in response["output"]["message"]["content"] if "text" in block)
    return {"json_string": text}
