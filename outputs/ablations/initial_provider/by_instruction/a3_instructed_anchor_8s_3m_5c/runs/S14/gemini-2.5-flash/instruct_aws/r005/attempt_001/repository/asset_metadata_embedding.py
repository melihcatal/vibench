import boto3
import json
from storage_models import AssetMetadataEmbeddingRequest, AssetMetadataEmbeddingResponse

def get_bedrock_runtime_client():
    return boto3.client('bedrock-runtime')

def asset_metadata_embedding(request: AssetMetadataEmbeddingRequest) -> AssetMetadataEmbeddingResponse:
    bedrock_runtime_client = get_bedrock_runtime_client()

    # Using Amazon Titan Embeddings G1 - Text on Amazon Bedrock
    model_id = "amazon.titan-embed-text-v1"

    # Combine metadata and extracted text for embedding
    text_to_embed = []
    if request.metadata:
        # Convert metadata dictionary to a string format suitable for embedding
        metadata_str = ", ".join([f"{k}: {v}" for k, v in request.metadata.items()])
        text_to_embed.append(f"Metadata: {metadata_str}")
    
    if request.extracted_text:
        text_to_embed.append(f"Document Text: {request.extracted_text}")

    input_text = "\n".join(text_to_embed)

    if not input_text:
        raise ValueError("No metadata or extracted text provided for embedding.")

    body = json.dumps({"inputText": input_text})

    response = bedrock_runtime_client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )

    response_body = json.loads(response.get('body').read())
    embedding = response_body.get('embedding')

    return AssetMetadataEmbeddingResponse(embedding=embedding)
