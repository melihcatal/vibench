import os
from typing import Any, Dict, List, Sequence

from openai import OpenAI


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def _embed_texts(texts: Sequence[str], model: str) -> List[List[float]]:
    response = _client().embeddings.create(model=model, input=list(texts))
    return [item.embedding for item in response.data]


def embed_for_search(query: str, documents: Sequence[str], model: str = "text-embedding-3-small") -> Dict[str, Any]:
    if not query:
        raise ValueError("query must not be empty")
    if not documents:
        raise ValueError("documents must not be empty")

    query_embedding = _embed_texts([query], model=model)[0]
    document_embeddings = _embed_texts(documents, model=model)

    return {
        "query": query,
        "query_embedding": query_embedding,
        "documents": list(documents),
        "document_embeddings": document_embeddings,
        "model": model,
    }
