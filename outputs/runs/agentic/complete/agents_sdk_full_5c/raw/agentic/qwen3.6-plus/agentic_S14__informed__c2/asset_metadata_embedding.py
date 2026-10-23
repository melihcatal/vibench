"""
asset_metadata_embedding.py - Embed object metadata and extracted text for
search using Amazon Titan Embeddings via Amazon Bedrock.

Uses the boto3 SDK (Amazon Bedrock Runtime) with model
amazon.titan-embed-text-v2:0.
Auth env vars: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""
from __future__ import annotations

import json
import os
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from storage_models import EmbeddingRequest, EmbeddingResponse, EmbeddingObject


def asset_metadata_embedding(
    texts: list[str],
    model_id: str = "amazon.titan-embed-text-v2:0",
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region: Optional[str] = None,
) -> EmbeddingResponse:
    """
    Generate vector embeddings for object metadata and extracted text using
    Amazon Bedrock with the Amazon Titan Embeddings model.

    Amazon Titan Embeddings converts text into high-dimensional vector
    representations suitable for similarity search, clustering, and
    retrieval-augmented generation (RAG) pipelines.

    Args:
        texts: List of text strings to embed (metadata, summaries, OCR text, etc.)
        model_id: Amazon Bedrock model ID (default: amazon.titan-embed-text-v2:0).
        aws_access_key_id: Optional AWS access key ID override.
        aws_secret_access_key: Optional AWS secret access key override.
        region: Optional AWS region override.

    Returns:
        EmbeddingResponse with generated vectors and token usage.
    """
    request = EmbeddingRequest(
        texts=texts,
        model_id=model_id,
    )

    bedrock_region = region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    bedrock_runtime = boto3.client(
        "bedrock-runtime",
        region_name=bedrock_region,
        aws_access_key_id=aws_access_key_id or os.environ.get("AWS_ACCESS_KEY_ID", ""),
        aws_secret_access_key=aws_secret_access_key or os.environ.get("AWS_SECRET_ACCESS_KEY", ""),
    )

    all_embeddings: list[EmbeddingObject] = []
    total_input_tokens = 0

    for index, text in enumerate(request.texts):
        if not text or not text.strip():
            all_embeddings.append(
                EmbeddingObject(index=index, embedding=[], text=text)
            )
            continue

        # Build the Amazon Titan Embeddings request body for Bedrock
        request_body = {
            "inputText": text.strip(),
            "dimensions": 1024,
            "normalize": True,
        }

        try:
            response = bedrock_runtime.invoke_model(
                modelId=request.model_id,
                contentType="application/json",
                accept="application/json",
                body=json.dumps(request_body),
            )

            response_body = json.loads(response["body"].read())

            embedding_vector = response_body.get("embedding", [])
            input_token_count = response_body.get("inputTextTokenCount", 0)
            total_input_tokens += input_token_count

            all_embeddings.append(
                EmbeddingObject(
                    index=index,
                    embedding=embedding_vector,
                    text=text,
                )
            )

        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "Unknown")
            error_message = e.response.get("Error", {}).get("Message", str(e))
            raise RuntimeError(
                f"Amazon Bedrock (amazon.titan-embed-text-v2:0) embedding error "
                f"[{error_code}]: {error_message}"
            )

    return EmbeddingResponse(
        model_id=request.model_id,
        embeddings=all_embeddings,
        input_token_count=total_input_tokens,
    )


def embed_document_with_metadata(
    document_text: str,
    metadata: dict,
    model_id: str = "amazon.titan-embed-text-v2:0",
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region: Optional[str] = None,
) -> EmbeddingResponse:
    """
    Create embeddings for a document by combining its extracted text with
    structured metadata into multiple embedding inputs.

    Produces embeddings for:
    1. The raw document text
    2. A combined metadata+text string for richer search

    Args:
        document_text: Extracted document text content.
        metadata: Dictionary of object metadata (bucket, key, content_type, etc.)
        model_id: Amazon Bedrock model ID (default: amazon.titan-embed-text-v2:0).
        aws_access_key_id: Optional AWS access key ID override.
        aws_secret_access_key: Optional AWS secret access key override.
        region: Optional AWS region override.

    Returns:
        EmbeddingResponse with embeddings for both text and combined inputs.
    """
    # Build text representations for embedding
    metadata_str = " ".join(f"{k}: {v}" for k, v in metadata.items())
    combined_text = f"{metadata_str}\n{document_text}"

    texts_to_embed = [document_text, combined_text]

    return asset_metadata_embedding(
        texts=texts_to_embed,
        model_id=model_id,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region=region,
    )
