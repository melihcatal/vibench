from __future__ import annotations

import os
from typing import Sequence

import requests

from embeddings_models import (
    EmbeddingRequest,
    EmbeddingResponse,
    normalize_texts,
    parse_embedding_response,
)


COHERE_API_URL = "https://api.cohere.com/v1/embed"
COHERE_API_KEY_ENV = "COHERE_API_KEY"
DEFAULT_EMBED_MODEL = "embed-english-v3.0"
DEFAULT_MULTILINGUAL_MODEL = "embed-multilingual-v3.0"


class CohereEmbeddingsClient:
    def __init__(self, api_key: str | None = None, timeout: float = 30.0) -> None:
        self.api_key = api_key or os.environ[COHERE_API_KEY_ENV]
        self.timeout = timeout

    def embed(
        self,
        texts: Sequence[str],
        model: str = DEFAULT_EMBED_MODEL,
        input_type: str = "search_document",
        truncate: str = "END",
        embedding_types: Sequence[str] | None = None,
    ) -> EmbeddingResponse:
        normalized = normalize_texts(texts)
        request = EmbeddingRequest(
            texts=normalized, model=model, input_type=input_type, truncate=truncate
        )
        payload = {
            "model": request.model,
            "texts": request.texts,
            "input_type": request.input_type,
            "truncate": request.truncate,
            "embedding_types": list(embedding_types or ["float"]),
        }
        response = requests.post(
            COHERE_API_URL,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return parse_embedding_response(response.json(), request.texts)
