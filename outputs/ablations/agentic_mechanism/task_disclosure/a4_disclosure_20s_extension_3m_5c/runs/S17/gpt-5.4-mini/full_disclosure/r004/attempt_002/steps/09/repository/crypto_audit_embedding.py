from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Iterable, Optional

import requests


OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_EMBEDDINGS_URL = "https://api.openai.com/v1/embeddings"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def _normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def _normalize_notes(notes: Any) -> list[str]:
    if notes is None:
        return []
    if isinstance(notes, str):
        text = notes.strip()
        return [text] if text else []
    if isinstance(notes, Iterable):
        result: list[str] = []
        for note in notes:
            text = _normalize_text(note)
            if text:
                result.append(text)
        return result
    text = _normalize_text(notes)
    return [text] if text else []


@dataclass(slots=True)
class CryptoAuditEmbeddingRequest:
    notes: list[str] = field(default_factory=list)
    model: str = OPENAI_EMBEDDING_MODEL

    def __post_init__(self) -> None:
        self.notes = _normalize_notes(self.notes)
        self.model = _normalize_text(self.model) or OPENAI_EMBEDDING_MODEL


@dataclass(slots=True)
class CryptoAuditEmbeddingResponse:
    model: str
    embeddings: list[list[float]]
    input_texts: list[str]


def _api_key(explicit_api_key: Optional[str] = None) -> str:
    api_key = explicit_api_key or os.getenv(OPENAI_API_KEY_ENV)
    if not api_key:
        raise ValueError(f"Missing required environment variable: {OPENAI_API_KEY_ENV}")
    return api_key


def embed_crypto_audit_notes(notes: Any, api_key: Optional[str] = None, model: str = OPENAI_EMBEDDING_MODEL, timeout: float = 30.0) -> CryptoAuditEmbeddingResponse:
    request = CryptoAuditEmbeddingRequest(notes=_normalize_notes(notes), model=model)
    if not request.notes:
        return CryptoAuditEmbeddingResponse(model=request.model, embeddings=[], input_texts=[])
    response = requests.post(
        OPENAI_EMBEDDINGS_URL,
        headers={
            "Authorization": f"Bearer {_api_key(api_key)}",
            "Content-Type": "application/json",
        },
        json={"model": request.model, "input": request.notes},
        timeout=timeout,
    )
    response.raise_for_status()
    payload = response.json()
    embeddings = [item["embedding"] for item in payload.get("data", [])]
    return CryptoAuditEmbeddingResponse(model=payload.get("model", request.model), embeddings=embeddings, input_texts=request.notes)


def build_embedding_index(notes: Any, api_key: Optional[str] = None, model: str = OPENAI_EMBEDDING_MODEL, timeout: float = 30.0) -> dict[str, Any]:
    result = embed_crypto_audit_notes(notes=notes, api_key=api_key, model=model, timeout=timeout)
    return {"provider": "openai", "model": result.model, "notes": result.input_texts, "embeddings": result.embeddings}
