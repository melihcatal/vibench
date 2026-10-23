"""
Embed transcript segments for semantic retrieval using AWS Bedrock.

Provider: AWS Bedrock (aws.bedrock)
SDK: boto3
Endpoint: bedrock-runtime.{region}.amazonaws.com
Model: cohere.embed-multilingual-v3 / amazon.titan-embed-text-v2:0
"""

import json
from typing import Optional

from speech_client import get_bedrock_runtime_client
from speech_models import Segment


COHERE_EMBED_MODEL_ID = "cohere.embed-multilingual-v3"
TITAN_EMBED_MODEL_ID = "amazon.titan-embed-text-v2:0"


def embed_transcript_segment(
    text: str,
    model_id: str = COHERE_EMBED_MODEL_ID,
    input_type: str = "search_document",
) -> dict:
    """
    Generate embedding vector for a single transcript segment using AWS Bedrock.

    Args:
        text: The text segment to embed
        model_id: Bedrock model ID for embedding
        input_type: Cohere input type (search_document, search_query, classification)

    Returns:
        dict with embedding vector and metadata
    """
    client = get_bedrock_runtime_client()

    if "cohere" in model_id:
        body = {
            "texts": [text],
            "input_type": input_type,
            "truncate": "END",
        }
    else:
        body = {
            "inputText": text,
            "dimensions": 1024,
            "normalize": True,
        }

    response = client.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(body),
    )

    response_body = json.loads(response["body"].read().decode("utf-8"))

    if "cohere" in model_id:
        embedding = response_body.get("embeddings", [[]])[0]
        embedding_type = response_body.get("embedding_type", "float")
    else:
        embedding = response_body.get("embedding", [])
        embedding_type = "float"

    return {
        "text": text,
        "embedding": embedding,
        "embedding_dimension": len(embedding),
        "model_id": model_id,
        "embedding_type": embedding_type,
    }


def embed_transcript_segments(
    segments: list[Segment],
    model_id: str = COHERE_EMBED_MODEL_ID,
    include_metadata: bool = True,
) -> list[dict]:
    """
    Generate embeddings for all transcript segments for semantic search.

    Args:
        segments: List of Segment objects to embed
        model_id: Bedrock embedding model ID
        include_metadata: Whether to include segment metadata

    Returns:
        list of dicts with embeddings and segment data
    """
    results = []

    for segment in segments:
        if not segment.text.strip():
            continue

        embedding_result = embed_transcript_segment(
            text=segment.text,
            model_id=model_id,
            input_type="search_document",
        )

        entry = {
            "segment_id": segment.segment_id,
            "text": segment.text,
            "embedding": embedding_result["embedding"],
            "embedding_dimension": embedding_result["embedding_dimension"],
            "model_id": model_id,
        }

        if include_metadata:
            entry["speaker"] = segment.speaker
            entry["start_time_ms"] = segment.start_time_ms
            entry["end_time_ms"] = segment.end_time_ms
            entry["confidence"] = segment.confidence
            entry["word_count"] = len(segment.text.split())

        results.append(entry)

    return results


def batch_embed_texts(
    texts: list[str],
    model_id: str = COHERE_EMBED_MODEL_ID,
) -> list[list[float]]:
    """
    Batch embed multiple texts using AWS Bedrock embedding models.

    Args:
        texts: List of text strings to embed
        model_id: Bedrock embedding model ID

    Returns:
        list of embedding vectors
    """
    client = get_bedrock_runtime_client()

    if "cohere" in model_id:
        body = {
            "texts": texts,
            "input_type": "search_document",
            "truncate": "END",
        }
        response = client.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(body),
        )
        response_body = json.loads(response["body"].read().decode("utf-8"))
        return response_body.get("embeddings", [])
    else:
        embeddings = []
        for text in texts:
            body = {
                "inputText": text,
                "dimensions": 1024,
                "normalize": True,
            }
            response = client.invoke_model(
                modelId=model_id,
                contentType="application/json",
                accept="application/json",
                body=json.dumps(body),
            )
            response_body = json.loads(response["body"].read().decode("utf-8"))
            embeddings.append(response_body.get("embedding", []))
        return embeddings


def prepare_for_vector_search(
    segments: list[Segment],
    model_id: str = TITAN_EMBED_MODEL_ID,
) -> dict:
    """
    Prepare transcript segments for storage in a vector database.

    Uses AWS Bedrock Titan embedding model for semantic search indexing.

    Args:
        segments: List of Segment objects
        model_id: Embedding model ID

    Returns:
        dict with vectors and metadata for vector DB ingestion
    """
    embeddings = embed_transcript_segments(segments, model_id=model_id)

    documents = []
    for emb in embeddings:
        doc = {
            "id": emb["segment_id"],
            "values": emb["embedding"],
            "metadata": {
                "speaker": emb.get("speaker", "unknown"),
                "text": emb["text"],
                "start_time_ms": emb.get("start_time_ms", 0),
                "end_time_ms": emb.get("end_time_ms", 0),
                "confidence": emb.get("confidence", 0),
                "model_id": model_id,
            },
        }
        documents.append(doc)

    return {
        "documents": documents,
        "vector_count": len(documents),
        "vector_dimension": embeddings[0]["embedding_dimension"] if embeddings else 0,
        "model_id": model_id,
    }
