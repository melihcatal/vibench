import json

from document_client import amazon_bedrock_client


def document_field_extraction(payload, config=None):
    client = amazon_bedrock_client(config)
    model_id = (config or {}).get("model_id", "anthropic.claude-3-haiku-20240307-v1:0")
    prompt = payload.get("text", "")
    body = json.dumps({"messages": [{"role": "user", "content": prompt}], "max_tokens": 256})
    response = client.invoke_model(modelId=model_id, body=body, contentType="application/json", accept="application/json")
    return {"model_id": model_id, "response": response.get("body").read().decode() if response.get("body") else ""}
