from document_client import get_bedrock_runtime_client


def ocr_embedding(payload, config=None):
    client = get_bedrock_runtime_client(config)
    model_id = config.get("model_id") if config else None
    model_id = model_id or "amazon.titan-embed-text-v1"
    text = payload.get("text", "")
    response = client.invoke_model(modelId=model_id, body=text.encode("utf-8"), contentType="text/plain", accept="application/json")
    return {"embedding": response.get("body", b"")}
