"""
Embed object metadata and extracted text for search.

Uses Amazon Bedrock with Titan Text Embeddings model as the concrete managed
embedding service. Generates vector embeddings from S3 object metadata and
document content for similarity search and retrieval.
"""

import hashlib
import json
import math
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError

from stored_document_ocr import TextractOCRResult, run_ocr_on_s3_object

# AWS Bedrock concrete embedding model identifiers
BEDROCK_TITAN_EMBED_TEXT_MODEL_ID = "amazon.titan-embed-text-v1"
BEDROCK_TITAN_EMBED_TEXT_V2_MODEL_ID = "amazon.titan-embed-text-v2:0"
BEDROCK_COHERE_EMBED_MODEL_ID = "cohere.embed-english-v3"
BEDROCK_SERVICE_ENDPOINT = "bedrock-runtime"


class EmbeddingResult:
    """Result from Amazon Bedrock embedding generation."""

    def __init__(
        self,
        embedding: List[float],
        model_id: str,
        input_tokens: int = 0,
        input_text_hash: Optional[str] = None,
        raw_response: Optional[Dict[str, Any]] = None,
    ):
        self.embedding = embedding
        self.model_id = model_id
        self.dimensions = len(embedding)
        self.input_tokens = input_tokens
        self.input_text_hash = input_text_hash
        self.raw_response = raw_response or {}

    def cosine_similarity(self, other: "EmbeddingResult") -> float:
        """Compute cosine similarity between this embedding and another."""
        if not self.embedding or not other.embedding:
            return 0.0
        dot_product = sum(a * b for a, b in zip(self.embedding, other.embedding))
        norm_a = math.sqrt(sum(a * a for a in self.embedding))
        norm_b = math.sqrt(sum(b * b for b in other.embedding))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot_product / (norm_a * norm_b)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_id": self.model_id,
            "dimensions": self.dimensions,
            "input_tokens": self.input_tokens,
            "input_text_hash": self.input_text_hash,
            "embedding_preview": self.embedding[:10],
        }


def _hash_input(text: str) -> str:
    """Create a deterministic hash of input text for caching/deduplication."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _build_metadata_embedding_text(
    metadata: Dict[str, Any],
    extracted_text: str = "",
    include_keys: Optional[List[str]] = None,
    max_metadata_text_length: int = 2000,
) -> str:
    """
    Build a combined text string from metadata and extracted content.

    Creates a structured text representation suitable for embedding generation.

    Args:
        metadata: Object metadata dictionary.
        extracted_text: Extracted document text.
        include_keys: Specific metadata keys to include (None for all).
        max_metadata_text_length: Max length for metadata portion.

    Returns:
        Combined text string for embedding.
    """
    parts = []

    if metadata:
        meta_parts = []
        for k, v in metadata.items():
            if include_keys and k not in include_keys:
                continue
            meta_parts.append(f"{k}: {v}")
        meta_text = " | ".join(meta_parts)
        if len(meta_text) > max_metadata_text_length:
            meta_text = meta_text[:max_metadata_text_length] + "..."
        parts.append(meta_text)

    if extracted_text:
        parts.append(extracted_text)

    return " ".join(parts)


def embed_text(
    text: str,
    model_id: str = BEDROCK_TITAN_EMBED_TEXT_V2_MODEL_ID,
    normalize: bool = True,
    dimensions: Optional[int] = None,
    client_config: Optional[Dict[str, Any]] = None,
) -> EmbeddingResult:
    """
    Generate a vector embedding for text using Amazon Bedrock Titan Embeddings.

    Uses the InvokeModel API with the Titan Text Embeddings model.

    Args:
        text: Text to embed.
        model_id: Bedrock embedding model identifier.
        normalize: Whether to normalize the embedding vector.
        dimensions: Optional output dimensions (for v2 model: 256, 512, 1024).
        client_config: Optional boto3 client configuration.

    Returns:
        EmbeddingResult with the vector and metadata.

    Raises:
        ClientError: If embedding generation fails.
        ModelTimeoutException: If the request times out.
    """
    if not text or not text.strip():
        return EmbeddingResult(
            embedding=[],
            model_id=model_id,
            input_text_hash=None,
        )

    bedrock_runtime = boto3.client(
        "bedrock-runtime",
        region_name=client_config.get("region_name") if client_config else None,
    )

    if "titan-embed-text-v2" in model_id:
        body: Dict[str, Any] = {
            "inputText": text,
            "dimensions": dimensions or 1024,
            "normalize": normalize,
        }
    else:
        body = {
            "inputText": text,
        }

    try:
        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            body=json.dumps(body),
        )

        response_body = json.loads(response.get("body").read())
        embedding = response_body.get("embedding", [])

        input_tokens = response_body.get("inputTextTokenCount", 0)

        return EmbeddingResult(
            embedding=embedding,
            model_id=model_id,
            input_tokens=input_tokens,
            input_text_hash=_hash_input(text),
            raw_response=response_body,
        )

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "")
        raise ClientError(
            e.response,
            f"Bedrock embedding failed with model {model_id}: {e} (code: {error_code})",
        )


def embed_object_metadata(
    bucket: str,
    key: str,
    metadata: Optional[Dict[str, Any]] = None,
    extracted_text: str = "",
    model_id: str = BEDROCK_TITAN_EMBED_TEXT_V2_MODEL_ID,
    normalize: bool = True,
    dimensions: Optional[int] = None,
    include_metadata_keys: Optional[List[str]] = None,
    client_config: Optional[Dict[str, Any]] = None,
) -> EmbeddingResult:
    """
    Generate an embedding from S3 object metadata and extracted text.

    Combines object metadata and document content into a single embedding
    vector suitable for semantic search.

    Args:
        bucket: S3 bucket name.
        key: S3 object key.
        metadata: Object metadata dictionary.
        extracted_text: Pre-extracted text content.
        model_id: Bedrock embedding model identifier.
        normalize: Whether to normalize the embedding.
        dimensions: Output dimensions for v2 model.
        include_metadata_keys: Specific metadata keys to include.
        client_config: Optional client configuration.

    Returns:
        EmbeddingResult for the combined metadata and content.
    """
    if metadata is None:
        metadata = {"bucket": bucket, "key": key}
    else:
        metadata = {"bucket": bucket, "key": key, **metadata}

    combined_text = _build_metadata_embedding_text(
        metadata=metadata,
        extracted_text=extracted_text,
        include_keys=include_metadata_keys,
    )

    return embed_text(
        text=combined_text,
        model_id=model_id,
        normalize=normalize,
        dimensions=dimensions,
        client_config=client_config,
    )


def embed_stored_document_full(
    bucket: str,
    key: str,
    model_id: str = BEDROCK_TITAN_EMBED_TEXT_V2_MODEL_ID,
    ocr_feature_types: Optional[List[str]] = None,
    client_config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Full pipeline: OCR a stored document and generate its embedding.

    Args:
        bucket: S3 bucket name.
        key: S3 object key.
        model_id: Bedrock embedding model identifier.
        ocr_feature_types: Textract features for OCR.
        client_config: Optional client configuration.

    Returns:
        Dictionary with OCR result, embedding, and metadata.
    """
    ocr_result = run_ocr_on_s3_object(
        bucket=bucket,
        key=key,
        feature_types=ocr_feature_types,
        client_config=client_config,
    )

    metadata = {
        "bucket": bucket,
        "key": key,
        "content_type": "document",
        "tables_count": len(ocr_result.detect_tables),
        "forms_count": len(ocr_result.detect_forms),
    }

    embedding = embed_object_metadata(
        bucket=bucket,
        key=key,
        metadata=metadata,
        extracted_text=ocr_result.get_full_text(),
        model_id=model_id,
        client_config=client_config,
    )

    return {
        "bucket": bucket,
        "key": key,
        "extracted_text": ocr_result.get_full_text(),
        "embedding": embedding.embedding,
        "embedding_model": embedding.model_id,
        "embedding_dimensions": embedding.dimensions,
        "input_tokens": embedding.input_tokens,
        "metadata": metadata,
        "text_hash": embedding.input_text_hash,
    }


def embed_batch_texts(
    texts: List[str],
    model_id: str = BEDROCK_TITAN_EMBED_TEXT_V2_MODEL_ID,
    normalize: bool = True,
    client_config: Optional[Dict[str, Any]] = None,
) -> List[EmbeddingResult]:
    """
    Generate embeddings for multiple text inputs.

    Args:
        texts: List of text strings to embed.
        model_id: Bedrock embedding model identifier.
        normalize: Whether to normalize embeddings.
        client_config: Optional client configuration.

    Returns:
        List of EmbeddingResult objects.
    """
    results = []
    for text in texts:
        if text and text.strip():
            result = embed_text(
                text=text,
                model_id=model_id,
                normalize=normalize,
                client_config=client_config,
            )
            results.append(result)
    return results


def find_similar_embeddings(
    query_text: str,
    candidate_texts: List[str],
    model_id: str = BEDROCK_TITAN_EMBED_TEXT_V2_MODEL_ID,
    top_k: int = 3,
    client_config: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """
    Find the most similar texts to a query using embeddings.

    Embeds the query and candidates, then ranks by cosine similarity.

    Args:
        query_text: Query text to search for.
        candidate_texts: List of candidate texts to compare against.
        model_id: Bedrock embedding model identifier.
        top_k: Number of top results to return.
        client_config: Optional client configuration.

    Returns:
        Ranked list of dicts with text, similarity score, and index.
    """
    query_embedding = embed_text(
        text=query_text,
        model_id=model_id,
        client_config=client_config,
    )

    scored = []
    for i, candidate in enumerate(candidate_texts):
        if candidate and candidate.strip():
            candidate_embedding = embed_text(
                text=candidate,
                model_id=model_id,
                client_config=client_config,
            )
            similarity = query_embedding.cosine_similarity(candidate_embedding)
            scored.append({
                "text": candidate,
                "similarity": similarity,
                "index": i,
            })

    scored.sort(key=lambda x: x["similarity"], reverse=True)
    return scored[:top_k]
