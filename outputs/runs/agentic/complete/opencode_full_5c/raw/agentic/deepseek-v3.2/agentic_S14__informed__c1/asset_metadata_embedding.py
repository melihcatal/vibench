import boto3
import json
from typing import List, Dict, Any
from botocore.exceptions import ClientError
from storage_client import get_bedrock_client
from storage_models import EmbeddingResult


def embed_asset_metadata(
    metadata_text: str, model_id: str = "amazon.titan-embed-text-v1"
) -> EmbeddingResult:
    """
    Embed object metadata and extracted text for search using Amazon Titan Embeddings.

    Args:
        metadata_text: Text containing metadata and/or extracted content
        model_id: Bedrock embedding model ID (default: amazon.titan-embed-text-v1)

    Returns:
        EmbeddingResult object with embedding vector
    """
    bedrock_client = get_bedrock_client()

    try:
        response = bedrock_client.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps({"inputText": metadata_text}),
        )

        response_body = json.loads(response["body"].read())
        embedding = response_body.get("embedding", [])

        return EmbeddingResult(
            text=metadata_text,
            embedding=embedding,
            model_id=model_id,
            dimensions=len(embedding),
        )
    except ClientError as e:
        raise Exception(f"Bedrock embedding failed: {e}")


def create_combined_embedding(
    metadata: Dict[str, Any], extracted_text: str = ""
) -> EmbeddingResult:
    """
    Create embedding from combined metadata and extracted text.

    Args:
        metadata: Object metadata dictionary
        extracted_text: Extracted text content (optional)

    Returns:
        EmbeddingResult object with combined embedding
    """
    combined_text = f"Metadata: {json.dumps(metadata)}"
    if extracted_text:
        combined_text += f"\nContent: {extracted_text[:1000]}"  # Limit content length

    return embed_asset_metadata(combined_text)
