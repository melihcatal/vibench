import boto3


def stored_asset_summary(payload, config=None):
    client = boto3.client("bedrock-runtime", region_name=(config or {}).get("region"))
    model_id = payload.get("model_id", "anthropic.claude-3-haiku-20240307-v1:0")
    prompt = payload["content"]
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": payload.get("max_tokens", 256),
        "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}],
    }
    return client.invoke_model(modelId=model_id, body=bytes(str(body).replace("'", '"'), "utf-8"))
