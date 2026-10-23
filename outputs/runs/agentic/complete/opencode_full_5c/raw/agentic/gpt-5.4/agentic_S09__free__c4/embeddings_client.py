from __future__ import annotations

import os
from typing import Sequence

import requests

from embeddings_models import (
    EmbeddingRequest,
    EmbeddingResponse,
    parse_embedding_response,
)


COHERE_API_URL = "https://api.cohere.com/v2/embed"
COHERE_EMBED_MODEL = os.getenv("COHERE_EMBED_MODEL", "embed-v4.0")
COHERE_API_KEY_ENV = "COHERE_API_KEY"


class CohereEmbeddingsClient:
    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        timeout: float = 30.0,
    ) -> None:
        self.api_key = api_key or os.getenv(COHERE_API_KEY_ENV)
        if not self.api_key:
            raise ValueError(f"Missing {COHERE_API_KEY_ENV}")
        self.model = model or COHERE_EMBED_MODEL
        self.timeout = timeout

    def embed(
        self, texts: Sequence[str], input_type: str | None = "search_document"
    ) -> EmbeddingResponse:
        request = EmbeddingRequest(
            texts=list(texts), model=self.model, input_type=input_type
        )
        response = requests.post(
            COHERE_API_URL,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json=request.as_payload(),
            timeout=self.timeout,
        )
        response.raise_for_status()
        return parse_embedding_response(response.json(), request.texts)


def get_embeddings_client(
    api_key: str | None = None, model: str | None = None, timeout: float = 30.0
) -> CohereEmbeddingsClient:
    return CohereEmbeddingsClient(api_key=api_key, model=model, timeout=timeout)
