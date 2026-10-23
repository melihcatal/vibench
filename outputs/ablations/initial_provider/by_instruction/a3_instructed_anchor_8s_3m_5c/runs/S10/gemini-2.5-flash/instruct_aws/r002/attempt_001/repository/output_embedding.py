import boto3
import json
from typing import List

def get_text_embedding(text: str) -> List[float]:
    """
    Embeds model outputs for clustering or retrieval using AWS Bedrock (Titan Embeddings).
    """
    bedrock_runtime = boto3.client(
        service_name="bedrock-runtime",
        region_name="us-east-1"
    )

    body = json.dumps({"inputText": text})
    model_id = "amazon.titan-embed-text-v1"
    content_type = "application/json"
    accept = "application/json"

    response = bedrock_runtime.invoke_model(
        body=body,
        modelId=model_id,
        contentType=content_type,
        accept=accept
    )

    response_body = json.loads(response.get("body").read())
    return response_body.get("embedding")

