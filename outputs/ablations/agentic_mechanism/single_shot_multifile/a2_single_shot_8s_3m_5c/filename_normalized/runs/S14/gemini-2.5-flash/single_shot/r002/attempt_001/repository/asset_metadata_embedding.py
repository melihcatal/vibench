import os
import json
import boto3
from storage_client import get_bedrock_runtime_client
from storage_models import AssetMetadataEmbeddingRequest, AssetMetadataEmbeddingResponse

def embed_asset_metadata(request: AssetMetadataEmbeddingRequest) -> AssetMetadataEmbeddingResponse:
    bedrock_runtime_client = get_bedrock_runtime_client()

    # Using AWS Bedrock with Amazon Titan Embeddings for creating embeddings
    # modelId: amazon.titan-embed-text-v1
    model_id = "amazon.titan-embed-text-v1"

    body = json.dumps({
        "inputText": request.text
    })

    response = bedrock_runtime_client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )

    response_body = json.loads(response.get('body').read())
    embedding = response_body.get('embedding', [])

    return AssetMetadataEmbeddingResponse(embedding=embedding)
