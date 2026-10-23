import boto3
import json
from model_client import get_bedrock_client

def embed_platform_output(
    text: str,
    embedding_model_id: str = "amazon.titan-embed-text-v1"
) -> dict:
    """
    Embeds platform outputs for evaluation or retrieval using AWS Bedrock embedding models.
    """
    client = get_bedrock_client()

    body = json.dumps({"inputText": text})

    response = client.invoke_model(
        body=body,
        modelId=embedding_model_id,
        accept="application/json",
        contentType="application/json"
    )

    response_body = json.loads(response.get("body").read())
    return response_body
