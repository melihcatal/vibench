import boto3
import json
from typing import List, Dict, Any, Optional
from storage_models import EmbeddingRequest, EmbeddingResponse, AssetMetadata
from object_metadata import get_object_metadata
from stored_document_ocr import run_ocr_on_stored_document
from stored_text_translate import translate_text
from stored_asset_summary import summarize_content


def generate_embedding(
    text: str, model: str = "amazon.titan-embed-text-v1"
) -> EmbeddingResponse:
    """
    Generate embeddings for text using AWS Bedrock embedding models.

    Args:
        text: Text to generate embedding for
        model: Embedding model ID (default: amazon.titan-embed-text-v1)

    Returns:
        EmbeddingResponse with embedding vector
    """
    if not text or not text.strip():
        return EmbeddingResponse(
            success=False,
            error_message="No text provided for embedding",
            provider="aws_bedrock",
        )

    # Truncate text if too long (embedding models have token limits)
    max_length = 8000  # Conservative limit for embedding models
    if len(text) > max_length:
        text = text[:max_length]

    try:
        # Initialize Bedrock runtime client
        bedrock_client = boto3.client("bedrock-runtime")

        # Prepare request based on model
        if model == "amazon.titan-embed-text-v1":
            # Titan Embed Text model
            request_body = {"inputText": text}

            response = bedrock_client.invoke_model(
                modelId=model,
                contentType="application/json",
                accept="application/json",
                body=json.dumps(request_body),
            )

            response_body = json.loads(response["body"].read())
            embedding = response_body.get("embedding", [])
            dimensions = len(embedding)

        elif model == "cohere.embed-english-v3":
            # Cohere Embed English model
            request_body = {"texts": [text], "input_type": "search_document"}

            response = bedrock_client.invoke_model(
                modelId=model,
                contentType="application/json",
                accept="application/json",
                body=json.dumps(request_body),
            )

            response_body = json.loads(response["body"].read())
            embedding = response_body.get("embeddings", [[]])[0]
            dimensions = len(embedding)

        else:
            return EmbeddingResponse(
                success=False,
                error_message=f"Unsupported embedding model: {model}",
                provider="aws_bedrock",
            )

        return EmbeddingResponse(
            success=True,
            embedding=embedding,
            model=model,
            dimensions=dimensions,
            provider="aws_bedrock",
        )

    except Exception as e:
        return EmbeddingResponse(
            success=False, error_message=str(e), provider="aws_bedrock"
        )


def embed_asset_metadata(bucket_name: str, object_key: str) -> AssetMetadata:
    """
    Embed object metadata and extracted text for search.

    Args:
        bucket_name: S3 bucket name
        object_key: Object key (path)

    Returns:
        AssetMetadata with embeddings and processed content
    """
    # Get object metadata
    metadata_result = get_object_metadata(bucket_name, object_key)
    if not metadata_result.success:
        raise ValueError(
            f"Failed to get object metadata: {metadata_result.error_message}"
        )

    # Initialize asset metadata
    asset = AssetMetadata(
        bucket=bucket_name,
        key=object_key,
        content_type=metadata_result.content_type or "application/octet-stream",
        size=metadata_result.size or 0,
        last_modified=metadata_result.last_modified or "",
        metadata=metadata_result.metadata,
    )

    # Extract text if document type
    content_type = asset.content_type.lower()
    extracted_text = ""

    if any(content_type.startswith(t) for t in ["application/pdf", "image/", "text/"]):
        ocr_result = run_ocr_on_stored_document(bucket_name, object_key)
        if ocr_result.success and ocr_result.text:
            extracted_text = ocr_result.text
            asset.extracted_text = extracted_text

    # Translate if needed (detect non-English)
    if extracted_text:
        # Simple language detection (in production would use proper detection)
        if any(
            word in extracted_text.lower()
            for word in ["el ", "la ", "los ", "las ", "un ", "una "]
        ):
            # Spanish-like text
            translate_result = translate_text(extracted_text, "auto", "en")
            if translate_result.success:
                extracted_text = translate_result.translated_text or extracted_text
                asset.language = "es->en"

        # Summarize content
        summary_result = summarize_content(extracted_text)
        if summary_result.success and summary_result.summary:
            asset.summary = summary_result.summary

    # Generate embedding from combined metadata and text
    embedding_text = f"""
    Bucket: {bucket_name}
    Key: {object_key}
    Content Type: {asset.content_type}
    Size: {asset.size} bytes
    Last Modified: {asset.last_modified}
    Summary: {asset.summary or "No summary available"}
    Extracted Text: {extracted_text[:500] if extracted_text else "No text extracted"}
    """

    # Generate embedding
    embedding_result = generate_embedding(embedding_text)
    if embedding_result.success and embedding_result.embedding:
        asset.embedding = embedding_result.embedding

    return asset


def batch_embed_assets(asset_list: List[Dict[str, str]]) -> List[AssetMetadata]:
    """
    Embed metadata for multiple assets.

    Args:
        asset_list: List of dictionaries with 'bucket' and 'key' keys

    Returns:
        List of AssetMetadata objects
    """
    results = []

    for asset_info in asset_list:
        try:
            bucket = asset_info.get("bucket")
            key = asset_info.get("key")

            if bucket and key:
                asset = embed_asset_metadata(bucket, key)
                results.append(asset)
        except Exception as e:
            print(f"Error embedding asset {asset_info}: {e}")

    return results


def search_similar_assets(
    query: str, asset_embeddings: List[AssetMetadata], top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Search for assets similar to query using vector similarity.

    Args:
        query: Search query text
        asset_embeddings: List of assets with embeddings
        top_k: Number of top results to return

    Returns:
        List of similar assets with similarity scores
    """
    # Generate embedding for query
    query_embedding_result = generate_embedding(query)
    if not query_embedding_result.success or not query_embedding_result.embedding:
        return []

    query_embedding = query_embedding_result.embedding

    # Calculate cosine similarity
    import numpy as np

    results = []
    for asset in asset_embeddings:
        if asset.embedding:
            # Convert to numpy arrays
            query_vec = np.array(query_embedding)
            asset_vec = np.array(asset.embedding)

            # Calculate cosine similarity
            similarity = np.dot(query_vec, asset_vec) / (
                np.linalg.norm(query_vec) * np.linalg.norm(asset_vec)
            )

            results.append({"asset": asset, "similarity": float(similarity)})

    # Sort by similarity (descending)
    results.sort(key=lambda x: x["similarity"], reverse=True)

    return results[:top_k]


def create_asset_index(assets: List[AssetMetadata]) -> Dict[str, Any]:
    """
    Create a search index from assets with embeddings.

    Args:
        assets: List of assets with embeddings

    Returns:
        Dictionary representing the search index
    """
    index = {
        "version": "1.0",
        "provider": "aws_bedrock",
        "model": "amazon.titan-embed-text-v1",
        "assets": [],
    }

    for asset in assets:
        asset_data = {
            "bucket": asset.bucket,
            "key": asset.key,
            "content_type": asset.content_type,
            "size": asset.size,
            "last_modified": asset.last_modified,
            "summary": asset.summary,
            "language": asset.language,
            "embedding_dimensions": len(asset.embedding) if asset.embedding else 0,
        }
        index["assets"].append(asset_data)

    return index


if __name__ == "__main__":
    # Example usage
    bucket = "my-documents-bucket"
    key = "reports/q1-report.pdf"

    try:
        # Embed single asset
        asset = embed_asset_metadata(bucket, key)
        print(f"Asset metadata embedded successfully")
        print(f"Bucket: {asset.bucket}")
        print(f"Key: {asset.key}")
        print(f"Content Type: {asset.content_type}")
        print(f"Size: {asset.size} bytes")
        print(f"Summary: {asset.summary[:100] if asset.summary else 'No summary'}")
        print(f"Embedding dimensions: {len(asset.embedding) if asset.embedding else 0}")

        # Generate embedding for a query
        query = "quarterly financial report"
        embedding_result = generate_embedding(query)
        print(f"\nQuery embedding generated: {embedding_result.success}")
        if embedding_result.success:
            print(f"Model: {embedding_result.model}")
            print(f"Dimensions: {embedding_result.dimensions}")

    except Exception as e:
        print(f"Error: {e}")
