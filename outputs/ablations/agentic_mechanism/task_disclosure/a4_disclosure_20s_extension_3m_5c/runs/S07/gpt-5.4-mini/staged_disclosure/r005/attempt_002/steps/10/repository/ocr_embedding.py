import os
from typing import Iterable, List, Sequence

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def _chunk_text(text: str, max_chars: int = 8000) -> List[str]:
    text = (text or "").strip()
    if not text:
        return []
    if len(text) <= max_chars:
        return [text]
    chunks: List[str] = []
    start = 0
    while start < len(text):
        end = min(len(text), start + max_chars)
        if end < len(text):
            split = text.rfind("\n", start, end)
            if split > start + max_chars // 2:
                end = split
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end
    return chunks


def sections_to_text(sections: Sequence[dict]) -> List[str]:
    texts: List[str] = []
    for section in sections:
        if not isinstance(section, dict):
            continue
        title = str(section.get("title", "")).strip()
        body = str(section.get("text", section.get("content", ""))).strip()
        combined = "\n".join(part for part in [title, body] if part)
        texts.extend(_chunk_text(combined))
    return texts


def embed_document_sections(sections: Sequence[dict], model: str = OPENAI_EMBEDDING_MODEL) -> List[List[float]]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    texts = sections_to_text(sections)
    if not texts:
        return []
    response = client.embeddings.create(model=model, input=texts)
    return [item.embedding for item in response.data]


def embed_query(query: str, model: str = OPENAI_EMBEDDING_MODEL) -> List[float]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model=model, input=[query])
    return response.data[0].embedding


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if not norm_a or not norm_b:
        return 0.0
    return dot / (norm_a * norm_b)


def rank_sections_by_query(sections: Sequence[dict], query: str, model: str = OPENAI_EMBEDDING_MODEL) -> List[dict]:
    texts = sections_to_text(sections)
    embeddings = embed_document_sections(sections, model=model)
    query_embedding = embed_query(query, model=model)
    scored = []
    for index, (section, embedding) in enumerate(zip(sections, embeddings)):
        score = cosine_similarity(query_embedding, embedding)
        scored.append({"index": index, "section": section, "score": score, "text": texts[index] if index < len(texts) else ""})
    return sorted(scored, key=lambda item: item["score"], reverse=True)
