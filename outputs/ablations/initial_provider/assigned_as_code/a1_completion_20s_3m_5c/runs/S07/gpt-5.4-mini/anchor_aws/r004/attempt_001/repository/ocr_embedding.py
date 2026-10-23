import json

from document_client import amazon_bedrock_client


def ocr_embedding(payload, config=None):
    client = amazon_bedrock_client(config)
    model_id = (config or {}).get("model_id", "amazon.titan-embed-text-v2:0")
    text = payload.get("text", "")
    response = client.invoke_model(modelId=model_id, body=json.dumps({"inputText": text}), contentType="application/json", accept="application/json")
    return {"model_id": model_id, "response": response.get("body").read().decode() if response.get("body") else ""}
