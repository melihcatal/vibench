from document_client import get_bedrock_runtime_client


def document_field_extraction(payload, config=None):
    client = get_bedrock_runtime_client(config)
    model_id = config.get("model_id") if config else None
    model_id = model_id or "anthropic.claude-3-haiku-20240307-v1:0"
    body = payload.get("text", "")
    response = client.invoke_model(modelId=model_id, body=body.encode("utf-8"), contentType="text/plain", accept="application/json")
    return {"fields": response.get("body", b"")}
