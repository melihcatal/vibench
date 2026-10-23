"""Embed object metadata and extracted text for search using Amazon Bedrock."""

import json
from typing import Optional, List

from storage_client import S3ClientFactory
from storage_models import EmbeddingRequest, EmbeddingResult


DEFAULT_EMBEDDING_MODEL_ID = "amazon.titan-embed-text-v2:0"


def embed_object_metadata_and_text(
    text: str,
    object_key: str = "",
    content_type: str = "",
    metadata: Optional[dict] = None,
    model_id: str = DEFAULT_EMBEDDING_MODEL_ID,
) -> EmbeddingResult:
    """
    Generate a vector embedding for object metadata and extracted text
    using Amazon Bedrock's Titan Embeddings model.

    Calls the Amazon Bedrock InvokeModel API against the
    bedrock-runtime.us-east-1.amazonaws.com endpoint with the
    'amazon.titan-embed-text-v2:0' model to produce a 1024-dimensional
    embedding vector suitable for vector search, semantic similarity,
    and retrieval-augmented generation (RAG) workflows.

    Args:
        text: The primary text content to embed (e.g., extracted or summarized text).
        object_key: S3 object key to include as context in the embedding input.
        content_type: MIME type of the source object.
        metadata: Additional S3 object metadata to incorporate.
        model_id: Bedrock embedding model identifier. Defaults to
                  'amazon.titan-embed-text-v2:0'.

    Returns:
        EmbeddingResult containing the embedding vector and model metadata.

    Raises:
        botocore.exceptions.ClientError: If the Bedrock model is unavailable
            or access is not configured.
    """
    factory = S3ClientFactory()
    bedrock_client = factory.get_bedrock_runtime_client()

    metadata_parts = []
    if object_key:
        metadata_parts.append(f"object_key: {object_key}")
    if content_type:
        metadata_parts.append(f"content_type: {content_type}")
    if metadata:
        for k, v in sorted(metadata.items()):
            metadata_parts.append(f"{k}: {v}")

    metadata_str = "\n".join(metadata_parts)

    if metadata_str and text:
        embed_input = f"{metadata_str}\n\n{text}"
    elif text:
        embed_input = text
    else:
        embed_input = metadata_str

    is_titan_v2 = "titan-embed-text-v2" in model_id

    if is_titan_v2:
        body = {
            "inputText": embed_input,
            "dimensions": 1024,
            "normalize": True,
        }
    elif "titan-embed-text-v1" in model_id:
        body = {
            "inputText": embed_input,
        }
    else:
        body = {
            "inputText": embed_input,
        }

    response = bedrock_client.invoke_model(
        modelId=model_id,
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json",
    )

    response_body = json.loads(response.get("body").read())

    embedding_vector = response_body.get("embedding", [])

    input_token_count = response_body.get("inputTextTokenCount", 0)

    return EmbeddingResult(
        vector=embedding_vector,
        model_id=model_id,
        input_token_count=input_token_count,
    )


def embed_batch_texts(
    texts: List[str],
    model_id: str = DEFAULT_EMBEDDING_MODEL_ID,
) -> List[EmbeddingResult]:
    """
    Generate embeddings for a list of text segments using Amazon Bedrock.

    Each text is embedded individually via the Titan embedding model
    on the bedrock-runtime endpoint. Amazon Bedrock does not currently
    support batch embedding in a single API call.

    Args:
        texts: List of text strings to embed.
        model_id: Bedrock embedding model ID.

    Returns:
        List of EmbeddingResult, one per input text.
    """
    results = []
    for text in texts:
        if not text or not text.strip():
            results.append(EmbeddingResult(
                vector=[],
                model_id=model_id,
                input_token_count=0,
            ))
            continue

        result = embed_object_metadata_and_text(
            text=text,
            model_id=model_id,
        )
        results.append(result)

    return results


def embed_with_cohere(
    text: str,
    model_id: str = "cohere.embed-english-v3",
) -> EmbeddingResult:
    """
    Generate an embedding using Cohere's embedding model on Amazon Bedrock.

    Uses the 'cohere.embed-english-v3' model via bedrock-runtime to produce
    a 1024-dimensional embedding vector optimized for English text.

    Args:
        text: Text content to embed.
        model_id: Cohere model identifier on Bedrock.

    Returns:
        EmbeddingResult with the Cohere embedding vector.
    """
    factory = S3ClientFactory()
    bedrock_client = factory.get_bedrock_runtime_client()

    body = {
        "texts": [text],
        "input_type": "search_document",
    }

    response = bedrock_client.invoke_model(
        modelId=model_id,
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json",
    )

    response_body = json.loads(response.get("body").read())
    embeddings = response_body.get("embeddings", [])

    return EmbeddingResult(
        vector=embeddings[0] if embeddings else [],
        model_id=model_id,
        input_token_count=0,
    )
