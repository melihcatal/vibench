from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence

from openai import OpenAI


DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


@dataclass
class EmbeddingSection:
    text: str
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class EmbeddedSection:
    text: str
    embedding: List[float]
    metadata: Dict[str, Any]


def get_client(api_key: Optional[str] = None) -> OpenAI:
    return OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))


def _section_text(section: Any) -> str:
    if isinstance(section, str):
        return section
    if isinstance(section, dict):
        return str(section.get("text", ""))
    return str(getattr(section, "text", ""))


def _section_metadata(section: Any) -> Dict[str, Any]:
    if isinstance(section, dict):
        meta = section.get("metadata")
        return dict(meta) if isinstance(meta, dict) else {}
    meta = getattr(section, "metadata", None)
    return dict(meta) if isinstance(meta, dict) else {}


def embed_sections(
    sections: Sequence[Any],
    model: str = DEFAULT_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
) -> List[EmbeddedSection]:
    client = get_client(api_key=api_key)
    texts = [_section_text(section) for section in sections]
    if not texts:
        return []
    response = client.embeddings.create(model=model, input=texts)
    embeddings = [item.embedding for item in response.data]
    return [
        EmbeddedSection(
            text=texts[i],
            embedding=embeddings[i],
            metadata=_section_metadata(sections[i]),
        )
        for i in range(len(texts))
    ]


def embed_document_text(
    text: str,
    model: str = DEFAULT_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
) -> EmbeddedSection:
    embedded = embed_sections([EmbeddingSection(text=text)], model=model, api_key=api_key)
    return embedded[0]
