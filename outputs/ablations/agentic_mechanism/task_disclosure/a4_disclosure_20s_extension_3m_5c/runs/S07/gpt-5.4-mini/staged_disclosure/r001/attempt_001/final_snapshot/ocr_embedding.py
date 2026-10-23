import os
from typing import Iterable, List, Sequence

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def _normalize_text(text: str) -> str:
    return " ".join(text.split()).strip()


def embed_sections(sections: Sequence[str], api_key: str | None = None) -> List[List[float]]:
    client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    cleaned = [_normalize_text(section) for section in sections if _normalize_text(section)]
    if not cleaned:
        return []
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=cleaned)
    return [item.embedding for item in response.data]


def embed_document_sections(sections: Iterable[str], api_key: str | None = None) -> List[List[float]]:
    return embed_sections(list(sections), api_key=api_key)
