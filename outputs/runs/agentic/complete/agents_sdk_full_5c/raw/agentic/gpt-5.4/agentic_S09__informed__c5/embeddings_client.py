from __future__ import annotations

import os
from typing import Sequence

import cohere

from embeddings_models import EmbeddingRequest, EmbeddingResult, ensure_texts

COHERE_EMBED_MODEL = os.getenv("COHERE_EMBED_MODEL", "embed-english-v3.0")
COHERE_DEFAULT_INPUT_TYPE = os.getenv("COHERE_INPUT_TYPE", "search_document")


class CohereEmbeddingsClient:
    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        self.api_key = api_key or os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("COHERE_API_KEY is required")
        self.model = model or COHERE_EMBED_MODEL
        self.client = cohere.ClientV2(api_key=self.api_key)

    def embed(self, request: EmbeddingRequest) -> EmbeddingResult:
        texts = ensure_texts(request.texts)
        response = self.client.embed(
            model=self.model,
            texts=texts,
            input_type=request.input_type or COHERE_DEFAULT_INPUT_TYPE,
            embedding_types=["float"],
            truncate=request.truncate,
        )
        embeddings = response.embeddings.float
        response_id = getattr(response, "id", None)
        return EmbeddingResult(
            embeddings=[list(vector) for vector in embeddings],
            model=self.model,
            response_id=response_id,
            meta={"provider": "cohere", "input_type": request.input_type},
        )

    def embed_texts(
        self,
        texts: Sequence[str] | str,
        *,
        input_type: str | None = None,
        truncate: str = "END",
    ) -> EmbeddingResult:
        request = EmbeddingRequest(
            texts=ensure_texts(texts),
            input_type=input_type or COHERE_DEFAULT_INPUT_TYPE,
            truncate=truncate,
        )
        return self.embed(request)
