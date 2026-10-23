import boto3

from model_client import get_bedrock_config
from model_models import normalize_text


def spoken_brief(payload, config=None):
    cfg = get_bedrock_config(config)
    client = boto3.client("bedrock-runtime", region_name=cfg["region"])
    text = normalize_text(payload.get("text", ""))
    response = client.converse(
        modelId=cfg["model_id"],
        messages=[{"role": "user", "content": [{"text": "Turn this into a brief spoken summary:\n\n" + text}]}],
    )
    output = "".join(block.get("text", "") for block in response["output"]["message"]["content"])
    return {"text": output}
