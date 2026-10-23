import boto3

from model_client import get_bedrock_config
from model_models import normalize_text


def stream_completion(payload, config=None):
    cfg = get_bedrock_config(config)
    client = boto3.client("bedrock-runtime", region_name=cfg["region"])
    prompt = normalize_text(payload.get("prompt", ""))
    response = client.converse_stream(
        modelId=cfg["model_id"],
        messages=[{"role": "user", "content": [{"text": prompt}]}],
    )
    chunks = []
    for event in response["stream"]:
        if "contentBlockDelta" in event and "text" in event["contentBlockDelta"].get("delta", {}):
            chunks.append(event["contentBlockDelta"]["delta"]["text"])
    return {"text": "".join(chunks), "chunks": chunks}
