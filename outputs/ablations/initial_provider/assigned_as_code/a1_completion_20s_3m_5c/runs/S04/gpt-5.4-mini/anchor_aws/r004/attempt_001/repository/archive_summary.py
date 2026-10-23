import boto3


def archive_summary(payload, config=None):
    client = boto3.client("bedrock-runtime", region_name=(config or {}).get("region"))
    prompt = payload["text"]
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 300,
        "messages": [{"role": "user", "content": [{"type": "text", "text": f"Summarize this transcript: {prompt}"}]}],
    }
    response = client.invoke_model(modelId=payload.get("model_id", "anthropic.claude-3-haiku-20240307-v1:0"), body=str(body))
    return {"summary": response.get("body", b"").decode("utf-8", errors="ignore") if hasattr(response.get("body", b""), "decode") else str(response.get("body", ""))}
