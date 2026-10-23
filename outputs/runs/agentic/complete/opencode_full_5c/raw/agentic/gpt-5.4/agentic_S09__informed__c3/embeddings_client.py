from __future__ import annotations

import os

import cohere

from embeddings_models import (
    EmbeddingResponse,
    build_embedding_request,
    parse_embedding_response,
)


DEFAULT_EMBED_MODEL = os.getenv("COHERE_EMBED_MODEL", "embed-english-v3.0")


def get_cohere_client() -> cohere.ClientV2:
    api_key = os.environ["COHERE_API_KEY"]
    return cohere.ClientV2(api_key=api_key)


def create_embeddings(
    texts: list[str], model: str | None = None, input_type: str = "search_document"
) -> EmbeddingResponse:
    resolved_model = model or DEFAULT_EMBED_MODEL
    request = build_embedding_request(
        texts=texts, model=resolved_model, input_type=input_type
    )
    client = get_cohere_client()
    response = client.embed(
        model=request.model,
        input_type=request.input_type,
        embedding_types=["float"],
        texts=request.texts,
    )
    return parse_embedding_response(response=response, model=request.model)
