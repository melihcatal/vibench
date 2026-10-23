import os
from typing import Iterable, List, Sequence

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def embed_translated_segments(segments: Sequence[str]) -> List[List[float]]:
    if not segments:
        return []
    response = _client().embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=list(segments))
    return [item.embedding for item in response.data]


def embed_translation_memory_rows(rows: Iterable[dict], text_key: str = "translated_segment") -> List[dict]:
    row_list = list(rows)
    texts = [str(row.get(text_key, "")) for row in row_list]
    vectors = embed_translated_segments(texts)
    enriched = []
    for row, vector in zip(row_list, vectors):
        updated = dict(row)
        updated["embedding"] = vector
        enriched.append(updated)
    return enriched
