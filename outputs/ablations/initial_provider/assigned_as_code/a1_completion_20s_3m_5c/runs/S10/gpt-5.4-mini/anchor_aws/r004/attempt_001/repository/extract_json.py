import json

import boto3

from model_client import get_bedrock_config
from model_models import normalize_text, payload_text


def extract_json(payload, config=None):
    cfg = get_bedrock_config(config)
    client = boto3.client("bedrock-runtime", region_name=cfg["region"])
    prompt = (
        "Extract the requested fields as strict JSON with no markdown.\n\n"
        + normalize_text(payload_text(payload))
    )
    response = client.converse(
        modelId=cfg["model_id"],
        messages=[{"role": "user", "content": [{"text": prompt}]}],
    )
    text = "".join(block.get("text", "") for block in response["output"]["message"]["content"])
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        data = {"text": text}
    return {"json": data, "text": text}
