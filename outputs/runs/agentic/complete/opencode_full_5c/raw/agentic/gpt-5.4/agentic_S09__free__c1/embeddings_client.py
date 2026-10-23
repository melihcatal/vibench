from __future__ import annotations

import os
from typing import Any

import requests

from embeddings_models import (
    EmbeddingRequest,
    EmbeddingResponse,
    parse_cohere_embeddings,
)


COHERE_API_BASE = "https://api.cohere.com/v2"
COHERE_EMBED_MODEL = os.getenv("COHERE_EMBED_MODEL", "embed-v4.0")


class CohereEmbeddingsClient:
    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        timeout: float = 30.0,
    ) -> None:
        self.api_key = api_key or os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("COHERE_API_KEY is required")
        self.model = model or COHERE_EMBED_MODEL
        self.timeout = timeout

    def embed(
        self,
        texts: list[str],
        input_type: str = "search_document",
        truncate: str = "END",
    ) -> EmbeddingResponse:
        request = EmbeddingRequest(
            texts=texts, input_type=input_type, truncate=truncate
        )
        response = requests.post(
            f"{COHERE_API_BASE}/embed",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json=request.to_payload(self.model),
            timeout=self.timeout,
        )
        response.raise_for_status()
        payload: dict[str, Any] = response.json()
        parsed = parse_cohere_embeddings(payload)
        return EmbeddingResponse(
            provider=parsed.provider,
            model=self.model,
            embeddings=parsed.embeddings,
            meta=parsed.meta,
        )
