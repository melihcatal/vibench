import os
from typing import Iterable, List, Sequence

from openai import OpenAI


EMBEDDING_MODEL = "text-embedding-3-small"


def _normalize_text(text: str) -> str:
    return " ".join(text.split()).strip()


def _chunk_sections(sections: Sequence[str]) -> List[str]:
    return [_normalize_text(section) for section in sections if _normalize_text(section)]


def embed_document_sections(sections: Sequence[str], model: str = EMBEDDING_MODEL) -> List[List[float]]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    cleaned_sections = _chunk_sections(sections)
    if not cleaned_sections:
        return []
    response = client.embeddings.create(model=model, input=cleaned_sections)
    return [item.embedding for item in response.data]


def embed_sections_with_metadata(sections: Iterable[dict], text_key: str = "text", model: str = EMBEDDING_MODEL) -> List[dict]:
    section_list = list(sections)
    texts = [_normalize_text(str(section.get(text_key, ""))) for section in section_list]
    payload = [text for text in texts if text]
    if not payload:
        return []
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(model=model, input=payload)
    vectors = [item.embedding for item in response.data]
    results: List[dict] = []
    vector_index = 0
    for section, text in zip(section_list, texts):
        if not text:
            continue
        results.append({**section, "embedding": vectors[vector_index]})
        vector_index += 1
    return results
