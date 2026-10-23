import boto3
import json
from document_client import get_bedrock_runtime_client


def ocr_embedding(payload, config=None):
    config = config or {}
    client = get_bedrock_runtime_client(region_name=config.get("region"))
    text_to_embed = payload["text"]
    model_id = config.get("embedding_model_id", "amazon.titan-embed-text-v1")  # Default Bedrock embedding model

    body = json.dumps({"inputText": text_to_embed})
    response = client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json",
    )
    response_body = json.loads(response.get("body").read())
    embedding = response_body.get("embedding")

    return {"embedding": embedding}
