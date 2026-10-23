import os
from typing import List, Optional
from openai import OpenAI
from embeddings_models import (
    EmbeddingRequest,
    EmbeddingResponse,
    BatchEmbeddingRequest,
    BatchEmbeddingResponse,
)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
DEFAULT_MODEL = "text-embedding-3-small"
DEFAULT_DIMENSIONS = 1536


def create_openai_client(api_key: Optional[str] = None) -> OpenAI:
    key = api_key or OPENAI_API_KEY
    if not key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=key)


def embed_single_text(
    text: str,
    model: str = DEFAULT_MODEL,
    dimensions: Optional[int] = None,
    client: Optional[OpenAI] = None,
) -> EmbeddingResponse:
    if client is None:
        client = create_openai_client()
    request = EmbeddingRequest(
        model=model,
        input_text=text,
        dimensions=dimensions,
    )
    response = client.embeddings.create(**request.to_payload())
    return EmbeddingResponse(
        embedding=response.data[0].embedding,
        model=response.model,
        usage_tokens=response.usage.total_tokens,
    )


def embed_batch_texts(
    texts: List[str],
    model: str = DEFAULT_MODEL,
    dimensions: Optional[int] = None,
    client: Optional[OpenAI] = None,
) -> BatchEmbeddingResponse:
    if client is None:
        client = create_openai_client()
    request = BatchEmbeddingRequest(
        model=model,
        input_texts=texts,
        dimensions=dimensions,
    )
    response = client.embeddings.create(**request.to_payload())
    embeddings = [item.embedding for item in response.data]
    models = [item.model for item in response.data]
    return BatchEmbeddingResponse(
        embeddings=embeddings,
        models=models,
        usage_tokens=response.usage.total_tokens,
    )


def embed_for_semantic_search(
    query: str,
    documents: List[str],
    model: str = DEFAULT_MODEL,
    dimensions: Optional[int] = None,
    client: Optional[OpenAI] = None,
):
    if client is None:
        client = create_openai_client()
    all_inputs = [query] + documents
    batch_request = BatchEmbeddingRequest(
        model=model,
        input_texts=all_inputs,
        dimensions=dimensions,
    )
    response = client.embeddings.create(**batch_request.to_payload())
    all_embeddings = [item.embedding for item in response.data]
    query_embedding = all_embeddings[0]
    document_embeddings = all_embeddings[1:]
    return query_embedding, document_embeddings
