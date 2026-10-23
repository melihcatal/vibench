import os
from typing import Iterable, List, Sequence

from openai import OpenAI


DEFAULT_EMBEDDING_MODEL = "text-embedding-3-large"


def _normalize_sections(sections: Iterable[str]) -> List[str]:
    normalized = []
    for section in sections:
        if section is None:
            continue
        text = str(section).strip()
        if text:
            normalized.append(text)
    return normalized


def embed_sections(
    sections: Sequence[str],
    model: str = DEFAULT_EMBEDDING_MODEL,
) -> List[List[float]]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    texts = _normalize_sections(sections)
    if not texts:
        return []
    response = client.embeddings.create(model=model, input=texts)
    return [item.embedding for item in response.data]


def embed_section(section: str, model: str = DEFAULT_EMBEDDING_MODEL) -> List[float]:
    embeddings = embed_sections([section], model=model)
    return embeddings[0] if embeddings else []
