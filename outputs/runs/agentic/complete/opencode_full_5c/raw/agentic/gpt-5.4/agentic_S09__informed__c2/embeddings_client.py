from __future__ import annotations

import os
from typing import Sequence

from openai import OpenAI

from embeddings_models import (
    EmbeddingRequest,
    EmbeddingResponse,
    parse_embedding_response,
)


def get_embeddings_client() -> OpenAI:
    api_key = os.environ["OPENAI_API_KEY"]
    base_url = os.getenv("OPENAI_BASE_URL")
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key=api_key)


def create_embeddings(texts: Sequence[str], model: str) -> EmbeddingResponse:
    request = EmbeddingRequest(texts=list(texts), model=model)
    client = get_embeddings_client()
    response = client.embeddings.create(input=request.texts, model=request.model)
    return parse_embedding_response(response)
