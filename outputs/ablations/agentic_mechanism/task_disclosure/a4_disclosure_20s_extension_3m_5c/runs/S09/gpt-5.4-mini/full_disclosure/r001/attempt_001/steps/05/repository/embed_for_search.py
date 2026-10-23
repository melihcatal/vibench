import os
from typing import List, Dict, Any

from openai import OpenAI


OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def _embed_texts(texts: List[str]) -> List[List[float]]:
    response = _client().embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=texts)
    return [item.embedding for item in response.data]


def embed_for_search(query: str, documents: List[str]) -> Dict[str, Any]:
    query_embedding = _embed_texts([query])[0]
    document_embeddings = _embed_texts(documents) if documents else []
    return {
        "provider": "openai",
        "model": OPENAI_EMBEDDING_MODEL,
        "query_embedding": query_embedding,
        "document_embeddings": document_embeddings,
    }
