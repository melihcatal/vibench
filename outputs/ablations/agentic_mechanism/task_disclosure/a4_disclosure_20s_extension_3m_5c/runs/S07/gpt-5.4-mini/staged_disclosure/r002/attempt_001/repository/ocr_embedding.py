import os
from typing import Iterable, List, Sequence

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")


def _normalize_sections(sections: Iterable[str]) -> List[str]:
    normalized = []
    for section in sections:
        if section is None:
            continue
        text = str(section).strip()
        if text:
            normalized.append(text)
    return normalized


def embed_document_sections(sections: Sequence[str], model: str = OPENAI_EMBEDDING_MODEL) -> List[List[float]]:
    client = OpenAI()
    normalized_sections = _normalize_sections(sections)
    if not normalized_sections:
        return []
    response = client.embeddings.create(model=model, input=normalized_sections)
    return [item.embedding for item in response.data]


def embed_section_with_metadata(section_text: str, metadata: dict | None = None, model: str = OPENAI_EMBEDDING_MODEL) -> dict:
    client = OpenAI()
    text = (section_text or "").strip()
    if not text:
        raise ValueError("section_text must be non-empty")
    response = client.embeddings.create(model=model, input=text)
    return {
        "text": text,
        "metadata": metadata or {},
        "model": model,
        "embedding": response.data[0].embedding,
    }
