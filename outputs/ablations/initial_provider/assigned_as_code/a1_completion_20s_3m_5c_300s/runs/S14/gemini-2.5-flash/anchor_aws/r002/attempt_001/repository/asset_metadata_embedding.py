import os
from storage_client import get_s3_client, get_openai_client
from storage_models import AssetMetadataEmbeddingRequest
from typing import List

def embed_asset_metadata(payload: AssetMetadataEmbeddingRequest, config: dict = None) -> dict:
    config = config or {}
    s3_client = get_s3_client(config)
    
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    
    openai_client = get_openai_client(openai_api_key)
    
    # Get object metadata
    head_response = s3_client.head_object(Bucket=config["bucket"], Key=payload.object_name)
    metadata = head_response.get("Metadata", {})
    content_type = head_response.get("ContentType", "")
    
    # Read the content of the object for text extraction if it's a text-like file
    text_content = ""
    if content_type.startswith("text/") or content_type == "application/json":
        obj = s3_client.get_object(Bucket=config["bucket"], Key=payload.object_name)
        text_content = obj['Body'].read().decode('utf-8')
    
    # Combine metadata and text content for embedding
    embedding_input = f"Object Name: {payload.object_name}\nContent Type: {content_type}\nMetadata: {metadata}\nContent: {text_content}"
    
    response = openai_client.embeddings.create(
        input=[embedding_input],
        model=payload.embedding_model
    )
    
    embedding = response.data[0].embedding
    
    return {"embedding": embedding}
