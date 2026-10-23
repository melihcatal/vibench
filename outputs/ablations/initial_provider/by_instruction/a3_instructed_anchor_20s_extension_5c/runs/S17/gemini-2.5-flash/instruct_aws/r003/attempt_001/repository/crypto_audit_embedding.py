import os
import boto3
import json
from security_models import EmbeddingRequest, EmbeddingResponse

def embed_crypto_audit_note(request: EmbeddingRequest) -> EmbeddingResponse:
    """
    Embeds a crypto audit note using AWS Bedrock's Titan Embeddings G1 - Text model.
    """
    bedrock_runtime_client = boto3.client("bedrock-runtime", region_name=os.environ.get("AWS_REGION", "us-east-1"))
    
    model_id = "amazon.titan-embed-text-v1"
    accept = "application/json"
    content_type = "application/json"

    body = json.dumps({"inputText": request.text})

    response = bedrock_runtime_client.invoke_model(
        body=body,
        modelId=model_id,
        accept=accept,
        contentType=content_type
    )
    
    response_body = json.loads(response.get('body').read())
    embedding = response_body.get('embedding')

    return EmbeddingResponse(
        embedding=embedding
    )
