from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional, Sequence

import requests

from document_models import NormalizedBlock, NormalizedLine, OCRResponse


OPENAI_EMBEDDINGS_URL = "https://api.openai.com/v1/embeddings"
DEFAULT_OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"


@dataclass(frozen=True)
class EmbeddingRequest:
    text: Optional[str] = None
    blocks: Sequence[Mapping[str, Any]] = field(default_factory=tuple)
    lines: Sequence[Mapping[str, Any]] = field(default_factory=tuple)
    model: str = DEFAULT_OPENAI_EMBEDDING_MODEL
    dimensions: Optional[int] = None

    @classmethod
    def from_ocr_response(cls, response: OCRResponse, model: str = DEFAULT_OPENAI_EMBEDDING_MODEL) -> "EmbeddingRequest":
        return cls(text=response.text, model=model)

    @classmethod
    def from_document_sections(
        cls,
        blocks: Sequence[NormalizedBlock],
        lines: Sequence[NormalizedLine],
        model: str = DEFAULT_OPENAI_EMBEDDING_MODEL,
    ) -> "EmbeddingRequest":
        return cls(blocks=tuple(blocks), lines=tuple(lines), model=model)

    def section_texts(self) -> Sequence[str]:
        sections = []
        if self.text:
            sections.append(self.text)
        for block in self.blocks:
            text = " ".join(line.get("text", "") for line in block.get("lines", []))
            if text:
                sections.append(text)
        for line in self.lines:
            text = str(line.get("text", "")).strip()
            if text:
                sections.append(text)
        return tuple(sections)


@dataclass(frozen=True)
class EmbeddingResponse:
    vectors: Sequence[Sequence[float]] = field(default_factory=tuple)
    raw: Mapping[str, Any] = field(default_factory=dict)


class OpenAIEmbeddingClient:
    def __init__(self, api_key: Optional[str] = None, timeout: float = 60.0) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.timeout = timeout

    def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        payload: Dict[str, Any] = {"input": list(request.section_texts()), "model": request.model}
        if request.dimensions is not None:
            payload["dimensions"] = request.dimensions
        headers = {"content-type": "application/json"}
        if self.api_key:
            headers["authorization"] = f"Bearer {self.api_key}"
        response = requests.post(OPENAI_EMBEDDINGS_URL, json=payload, headers=headers, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()
        vectors = [item.get("embedding", []) for item in data.get("data", [])]
        return EmbeddingResponse(vectors=tuple(tuple(float(v) for v in vector) for vector in vectors), raw=data)


def embed_document_sections(
    response: OCRResponse,
    model: str = DEFAULT_OPENAI_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
    timeout: float = 60.0,
) -> EmbeddingResponse:
    client = OpenAIEmbeddingClient(api_key=api_key, timeout=timeout)
    return client.embed(EmbeddingRequest.from_ocr_response(response, model=model))
