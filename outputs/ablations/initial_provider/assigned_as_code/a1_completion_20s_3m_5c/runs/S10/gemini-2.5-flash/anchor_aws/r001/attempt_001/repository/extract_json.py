import boto3
import json


def extract_json(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    prompt = "Extract JSON from the following text:\n\n" + payload["text"] + "\n\nProvide only the JSON output."
    response = client.converse(
        modelId="amazon.nova-pro-v1:0",
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"maxTokens": 2048},
    )
    text = "".join(block["text"] for block in response["output"]["message"]["content"] if "text" in block)
    try:
        return {"json_output": json.loads(text)}
    except json.JSONDecodeError:
        return {"json_output": {}}
