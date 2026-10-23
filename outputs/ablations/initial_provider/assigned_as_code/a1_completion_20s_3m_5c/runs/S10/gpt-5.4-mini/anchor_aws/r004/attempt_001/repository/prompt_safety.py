import boto3

from model_client import get_bedrock_config
from model_models import normalize_text


def prompt_safety(payload, config=None):
    cfg = get_bedrock_config(config)
    client = boto3.client("bedrock-runtime", region_name=cfg["region"])
    prompt = normalize_text(payload.get("text", ""))
    response = client.converse(
        modelId=cfg["model_id"],
        messages=[{"role": "user", "content": [{"text": "Assess whether the following text is unsafe. Return JSON with unsafe and rationale.\n\n" + prompt}]}],
    )
    text = "".join(block.get("text", "") for block in response["output"]["message"]["content"])
    return {"text": text}
