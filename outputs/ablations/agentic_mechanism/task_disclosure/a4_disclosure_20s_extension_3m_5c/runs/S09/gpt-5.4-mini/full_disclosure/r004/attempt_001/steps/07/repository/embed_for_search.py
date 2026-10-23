import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def _get_client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def _get_model() -> str:
    return os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def embed_for_search(query: str, documents: List[str], normalize: bool = True) -> Dict[str, Any]:
    client = _get_client()
    model = _get_model()
    inputs = [query] + documents
    response = client.embeddings.create(model=model, input=inputs)
    vectors = [item.embedding for item in response.data]
    if normalize:
        vectors = [_normalize(vec) for vec in vectors]
    return {"query_embedding": vectors[0], "document_embeddings": vectors[1:], "model": model}


def _normalize(vector: List[float]) -> List[float]:
    norm = sum(x * x for x in vector) ** 0.5
    if not norm:
        return vector
    return [x / norm for x in vector]
