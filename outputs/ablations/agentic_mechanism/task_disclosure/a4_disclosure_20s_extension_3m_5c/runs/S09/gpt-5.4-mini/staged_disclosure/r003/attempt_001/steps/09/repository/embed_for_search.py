import os
from typing import List, Sequence

from openai import OpenAI


DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


def _client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required")
    return OpenAI(api_key=api_key)


def embed_query(query: str, model: str = DEFAULT_EMBEDDING_MODEL) -> List[float]:
    response = _client().embeddings.create(model=model, input=query)
    return list(response.data[0].embedding)


def embed_documents(documents: Sequence[str], model: str = DEFAULT_EMBEDDING_MODEL) -> List[List[float]]:
    if not documents:
        return []
    response = _client().embeddings.create(model=model, input=list(documents))
    return [list(item.embedding) for item in response.data]


def embed_for_search(query: str, documents: Sequence[str], model: str = DEFAULT_EMBEDDING_MODEL):
    return {
        "query_embedding": embed_query(query, model=model),
        "document_embeddings": embed_documents(documents, model=model),
    }
