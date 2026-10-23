import boto3

from model_client import get_bedrock_config
from model_models import normalize_text


def result_translate(payload, config=None):
    cfg = get_bedrock_config(config)
    client = boto3.client("bedrock-runtime", region_name=cfg["region"])
    target_language = normalize_text(payload.get("language", "Spanish"))
    text = normalize_text(payload.get("text", ""))
    response = client.converse(
        modelId=cfg["model_id"],
        messages=[{"role": "user", "content": [{"text": f"Translate the following text into {target_language}:\n\n{text}"}]}],
    )
    output = "".join(block.get("text", "") for block in response["output"]["message"]["content"])
    return {"text": output}
