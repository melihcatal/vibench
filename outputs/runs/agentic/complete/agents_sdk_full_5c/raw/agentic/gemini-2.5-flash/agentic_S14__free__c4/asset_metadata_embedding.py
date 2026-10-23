import json
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from storage_client import get_bedrock_runtime_client

@dataclass
class AssetMetadataEmbeddingRequest:
    text_to_embed: str
    model_id: str = "amazon.titan-embed-text-v1"

@dataclass
class AssetMetadataEmbeddingResponse:
    success: bool
    message: str
    embedding: Optional[List[float]] = None
    input_token_count: Optional[int] = None

def embed_asset_metadata_and_text(
    request: AssetMetadataEmbeddingRequest
) -> AssetMetadataEmbeddingResponse:
    """
    Embeds object metadata and extracted text for search using AWS Bedrock (Titan Embeddings).
    """
    bedrock_runtime = get_bedrock_runtime_client()

    try:
        body = json.dumps({"inputText": request.text_to_embed})

        response = bedrock_runtime.invoke_model(
            body=body,
            modelId=request.model_id,
            accept="application/json",
            contentType="application/json"
        )

        response_body = json.loads(response.get("body").read())
        embedding = response_body.get("embedding")
        # Some models might return usage information, adding a placeholder if available
        input_token_count = response_body.get("inputTextTokenCount") # Titan specific

        if embedding is None:
            return AssetMetadataEmbeddingResponse(success=False, message="Embedding not found in response")

        return AssetMetadataEmbeddingResponse(
            success=True,
            message="Text embedded successfully",
            embedding=embedding,
            input_token_count=input_token_count
        )
    except Exception as e:
        return AssetMetadataEmbeddingResponse(success=False, message=f"Error creating embedding with Bedrock: {str(e)}")
