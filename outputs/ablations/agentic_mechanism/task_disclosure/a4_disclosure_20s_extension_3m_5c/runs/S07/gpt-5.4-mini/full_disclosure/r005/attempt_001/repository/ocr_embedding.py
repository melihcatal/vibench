from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Sequence

from openai import OpenAI


DEFAULT_OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


@dataclass
class DocumentSection:
    text: str
    section_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class EmbeddedSection:
    text: str
    embedding: List[float]
    section_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    fingerprint: Optional[str] = None


def _client(api_key: Optional[str] = None) -> OpenAI:
    return OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))


def _fingerprint(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _to_text(section: Any) -> str:
    if isinstance(section, str):
        return section
    if hasattr(section, "text"):
        return str(getattr(section, "text"))
    return str(section)


def embed_document_sections(
    sections: Sequence[Any],
    model: str = DEFAULT_OPENAI_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
) -> List[EmbeddedSection]:
    client = _client(api_key)
    texts = [_to_text(section) for section in sections]
    if not texts:
        return []
    response = client.embeddings.create(model=model, input=texts)
    embeddings = [item.embedding for item in response.data]
    result: List[EmbeddedSection] = []
    for section, text, embedding in zip(sections, texts, embeddings):
        section_id = getattr(section, "section_id", None) if not isinstance(section, str) else None
        metadata = getattr(section, "metadata", None) if not isinstance(section, str) else None
        result.append(
            EmbeddedSection(
                text=text,
                embedding=list(embedding),
                section_id=section_id,
                metadata=metadata,
                fingerprint=_fingerprint(text),
            )
        )
    return result


def embed_document_text(
    text: str,
    model: str = DEFAULT_OPENAI_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
) -> EmbeddedSection:
    embedded = embed_document_sections([text], model=model, api_key=api_key)
    return embedded[0]


def semantic_similarity(vector_a: Sequence[float], vector_b: Sequence[float]) -> float:
    if len(vector_a) != len(vector_b):
        raise ValueError("Embedding vectors must have the same length")
    dot = sum(a * b for a, b in zip(vector_a, vector_b))
    norm_a = sum(a * a for a in vector_a) ** 0.5
    norm_b = sum(b * b for b in vector_b) ** 0.5
    if not norm_a or not norm_b:
        return 0.0
    return dot / (norm_a * norm_b)


def rank_sections_by_query(
    sections: Sequence[Any],
    query: str,
    model: str = DEFAULT_OPENAI_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
) -> List[EmbeddedSection]:
    embedded_sections = embed_document_sections(sections, model=model, api_key=api_key)
    query_embedding = embed_document_text(query, model=model, api_key=api_key).embedding
    scored = [
        (semantic_similarity(item.embedding, query_embedding), item)
        for item in embedded_sections
    ]
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [item for _, item in scored]
