import json
import boto3
import os
from typing import List, Dict, Any, Optional
from botocore.exceptions import ClientError
from storage_client import get_bedrock_client
from storage_models import EmbeddingResult, ObjectMetadata
from object_metadata import get_object_metadata


def embed_text_with_titan(text: str) -> EmbeddingResult:
    """
    Embed text using Amazon Titan Embeddings via Bedrock.

    Args:
        text: Text to embed

    Returns:
        EmbeddingResult with embedding vector
    """
    bedrock_client = get_bedrock_client()

    # Titan Embeddings model ID
    model_id = "amazon.titan-embed-text-v1"

    try:
        # Prepare request body for Titan Embeddings
        body = json.dumps({"inputText": text})

        # Invoke the model
        response = bedrock_client.invoke_model(
            modelId=model_id,
            body=body,
            contentType="application/json",
            accept="application/json",
        )

        # Parse the response
        response_body = json.loads(response["body"].read())

        if "embedding" in response_body:
            embedding = response_body["embedding"]
            dimensions = len(embedding)
            return EmbeddingResult(
                success=True,
                embedding=embedding,
                model_id=model_id,
                dimensions=dimensions,
            )
        else:
            return EmbeddingResult(success=False, error="No embedding in response")

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_msg = e.response["Error"]["Message"]
        return EmbeddingResult(
            success=False, error=f"Bedrock error ({error_code}): {error_msg}"
        )
    except Exception as e:
        return EmbeddingResult(success=False, error=f"Unexpected error: {str(e)}")


def embed_object_metadata(bucket_name: str, object_key: str) -> EmbeddingResult:
    """
    Embed object metadata and extracted text for search.

    Args:
        bucket_name: S3 bucket name
        object_key: S3 object key

    Returns:
        EmbeddingResult with embedding vector
    """
    try:
        # Get object metadata
        metadata = get_object_metadata(bucket_name, object_key)

        # Try to extract text from document if it's a text-based file
        extracted_text = ""
        content_type = metadata.content_type.lower() if metadata.content_type else ""

        if any(
            text_type in content_type
            for text_type in [
                "text/",
                "pdf",
                "document",
                "msword",
                "vnd.openxmlformats",
            ]
        ):
            from stored_document_ocr import extract_text_from_s3_document

            ocr_result = extract_text_from_s3_document(bucket_name, object_key)
            if ocr_result.success and ocr_result.text:
                extracted_text = ocr_result.text[:1000]  # Limit text for embedding

        # Create text for embedding
        text_to_embed = f"""
        Object Key: {metadata.key}
        Bucket: {metadata.bucket}
        Content Type: {metadata.content_type}
        Size: {metadata.size} bytes
        Storage Class: {metadata.storage_class}
        Custom Metadata: {metadata.metadata}
        Extracted Text: {extracted_text}
        """

        # Generate embedding
        return embed_text_with_titan(text_to_embed.strip())

    except Exception as e:
        return EmbeddingResult(
            success=False, error=f"Error processing object metadata: {str(e)}"
        )


def batch_embed_texts(texts: List[str]) -> List[EmbeddingResult]:
    """
    Embed multiple texts in batch.

    Args:
        texts: List of texts to embed

    Returns:
        List of EmbeddingResult objects
    """
    results = []
    for text in texts:
        result = embed_text_with_titan(text)
        results.append(result)
    return results


def create_search_index_entry(bucket_name: str, object_key: str) -> Dict[str, Any]:
    """
    Create a search index entry with metadata and embedding.

    Args:
        bucket_name: S3 bucket name
        object_key: S3 object key

    Returns:
        Dictionary with search index entry
    """
    try:
        # Get metadata
        metadata = get_object_metadata(bucket_name, object_key)

        # Generate embedding
        embedding_result = embed_object_metadata(bucket_name, object_key)

        if not embedding_result.success:
            raise Exception(f"Failed to generate embedding: {embedding_result.error}")

        # Create search entry
        entry = {
            "id": f"{bucket_name}/{object_key}",
            "bucket": bucket_name,
            "key": object_key,
            "content_type": metadata.content_type,
            "size": metadata.size,
            "last_modified": metadata.last_modified.isoformat()
            if metadata.last_modified
            else None,
            "storage_class": metadata.storage_class,
            "metadata": metadata.metadata,
            "embedding": embedding_result.embedding,
            "embedding_model": embedding_result.model_id,
            "embedding_dimensions": embedding_result.dimensions,
        }

        return {"success": True, "entry": entry}

    except Exception as e:
        return {"success": False, "error": str(e)}


def similarity_search(
    query: str, embeddings: List[List[float]], top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Perform similarity search between query and embeddings.

    Args:
        query: Search query text
        embeddings: List of embedding vectors to search against
        top_k: Number of top results to return

    Returns:
        List of similarity scores and indices
    """
    # Generate query embedding
    query_result = embed_text_with_titan(query)

    if not query_result.success or not query_result.embedding:
        return []

    query_embedding = query_result.embedding

    # Calculate cosine similarity
    import numpy as np

    query_norm = np.linalg.norm(query_embedding)
    similarities = []

    for i, emb in enumerate(embeddings):
        if emb is None:
            continue

        emb_norm = np.linalg.norm(emb)
        if query_norm > 0 and emb_norm > 0:
            dot_product = np.dot(query_embedding, emb)
            similarity = dot_product / (query_norm * emb_norm)
            similarities.append((i, similarity))

    # Sort by similarity (descending)
    similarities.sort(key=lambda x: x[1], reverse=True)

    # Return top-k results
    return [{"index": idx, "similarity": sim} for idx, sim in similarities[:top_k]]
