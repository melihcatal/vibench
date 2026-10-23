import boto3

from model_client import get_bedrock_config
from model_models import normalize_text


def answer_with_context(payload, config=None):
    cfg = get_bedrock_config(config)
    client = boto3.client("bedrock-runtime", region_name=cfg["region"])
    context = normalize_text(payload.get("context", ""))
    question = normalize_text(payload.get("question", ""))
    prompt = f"Answer the question using only the context.\n\nContext:\n{context}\n\nQuestion:\n{question}"
    response = client.converse(
        modelId=cfg["model_id"],
        messages=[{"role": "user", "content": [{"text": prompt}]}],
    )
    text = "".join(block.get("text", "") for block in response["output"]["message"]["content"])
    return {"text": text}
