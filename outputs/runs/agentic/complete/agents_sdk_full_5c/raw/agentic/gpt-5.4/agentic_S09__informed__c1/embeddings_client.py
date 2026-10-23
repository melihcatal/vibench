from __future__ import annotations

import os
from typing import Sequence

from openai import OpenAI

from embeddings_models import EmbeddingRecord, EmbeddingRequest, EmbeddingResponse, normalize_texts

DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required for OpenAI embeddings")
    base_url = os.getenv("OPENAI_BASE_URL")
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key=api_key)


def build_embedding_request(
    texts: Sequence[str],
    model: str | None = None,
    input_type: str = "search_document",
) -> EmbeddingRequest:
    return EmbeddingRequest.from_texts(texts=texts, model=model or DEFAULT_EMBEDDING_MODEL, input_type=input_type)


def create_embeddings(
    texts: Sequence[str],
    model: str | None = None,
    dimensions: int | None = None,
    input_type: str = "search_document",
) -> EmbeddingResponse:
    request = build_embedding_request(texts=texts, model=model, input_type=input_type)
    client = get_openai_client()
    params = {
        "model": request.model,
        "input": normalize_texts(request.texts),
    }
    if dimensions is not None:
        params["dimensions"] = dimensions
    response = client.embeddings.create(**params)
    records = [
        EmbeddingRecord(index=item.index, embedding=list(item.embedding), text=request.texts[item.index])
        for item in response.data
    ]
    usage = {}
    if getattr(response, "usage", None) is not None:
        usage = {
            key: value
            for key, value in response.usage.model_dump().items()
            if value is not None
        }
    return EmbeddingResponse(model=response.model, records=records, usage=usage)
