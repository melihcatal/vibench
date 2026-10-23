import boto3
from document_models import normalize_text


def ocr_embedding(payload, config=None):
    region = (config or {}).get("region")
    client = boto3.client("bedrock-runtime", region_name=region)
    text = normalize_text(payload.get("text"))
    model_id = (config or {}).get("model_id", "amazon.titan-embed-text-v2:0")
    response = client.invoke_model(modelId=model_id, body=("{\"inputText\": \"" + text.replace("\\", "\\\\").replace('"', '\\"') + "\"}").encode())
    return {"embedding_response": response.get("body").read()}
