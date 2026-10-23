import json

from model_client import get_bedrock_client, get_model_id


def extract_json(payload, config=None):
    client = get_bedrock_client(config)
    prompt = "Extract structured JSON from the following text. Return only valid JSON.\n\n" + payload["text"]
    response = client.converse(
        modelId=get_model_id(config),
        messages=[{"role": "user", "content": [{"text": prompt}]}],
    )
    text = "".join(block["text"] for block in response["output"]["message"]["content"] if "text" in block)
    return {"json": json.loads(text)}
