import boto3

from storage_client import load_storage_config


def stored_asset_summary(payload, config=None):
    cfg = load_storage_config(config)
    client = boto3.client("bedrock-runtime", region_name=cfg["region"])
    content = payload.get("text") or payload.get("content") or ""
    model_id = payload.get("model_id", "anthropic.claude-3-haiku-20240307-v1:0")
    prompt = f"Summarize this asset briefly:\n\n{content}"
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 300,
        "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}],
    }
    response = client.invoke_model(modelId=model_id, body=bytes(str(body), "utf-8"))
    return {"model_id": model_id, "summary": response.get("body")}
