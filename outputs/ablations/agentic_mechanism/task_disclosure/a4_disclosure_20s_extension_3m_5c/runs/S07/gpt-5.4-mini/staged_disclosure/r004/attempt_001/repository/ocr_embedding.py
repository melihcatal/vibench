import os
from typing import Any, Dict, Iterable, List, Optional, Sequence

from openai import OpenAI


class OCREmbeddingClient:
    def __init__(self, api_key: Optional[str] = None, model: str = "text-embedding-3-small"):
        self.client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))
        self.model = model

    def embed_section(self, section_text: str) -> List[float]:
        text = (section_text or "").strip()
        if not text:
            return []
        response = self.client.embeddings.create(model=self.model, input=text)
        return list(response.data[0].embedding)

    def embed_sections(self, sections: Sequence[str]) -> List[List[float]]:
        cleaned = [(section or "").strip() for section in sections]
        payload = [section for section in cleaned if section]
        if not payload:
            return [[] for _ in sections]
        response = self.client.embeddings.create(model=self.model, input=payload)
        embeddings = [list(item.embedding) for item in response.data]
        iterator = iter(embeddings)
        results: List[List[float]] = []
        for section in cleaned:
            results.append(next(iterator) if section else [])
        return results


def embed_document_sections(sections: Sequence[Dict[str, Any]], api_key: Optional[str] = None, model: str = "text-embedding-3-small") -> List[Dict[str, Any]]:
    client = OCREmbeddingClient(api_key=api_key, model=model)
    texts = [str(section.get("text", "")) for section in sections]
    embeddings = client.embed_sections(texts)
    enriched: List[Dict[str, Any]] = []
    for section, embedding in zip(sections, embeddings):
        updated = dict(section)
        updated["embedding"] = embedding
        updated["embedding_model"] = model
        enriched.append(updated)
    return enriched


def semantic_retrieve(query: str, embedded_sections: Sequence[Dict[str, Any]], api_key: Optional[str] = None, model: str = "text-embedding-3-small", top_k: int = 5) -> List[Dict[str, Any]]:
    client = OCREmbeddingClient(api_key=api_key, model=model)
    query_embedding = client.embed_section(query)
    if not query_embedding:
        return []

    def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(x * x for x in b) ** 0.5
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    scored = []
    for section in embedded_sections:
        embedding = section.get("embedding") or []
        if embedding:
            scored.append((cosine_similarity(query_embedding, embedding), section))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [section for _, section in scored[:top_k]]
