import os
from typing import Iterable, List, Sequence

from openai import OpenAI


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def embed_query(query: str) -> List[float]:
    response = _client().embeddings.create(model="text-embedding-3-small", input=query)
    return response.data[0].embedding


def embed_documents(documents: Sequence[str]) -> List[List[float]]:
    response = _client().embeddings.create(model="text-embedding-3-small", input=list(documents))
    return [item.embedding for item in response.data]


if __name__ == "__main__":
    import sys

    args = sys.argv[1:]
    if not args:
        raise SystemExit("usage: embed_for_search.py <query> [document ...]")

    query = args[0]
    docs = args[1:]
    print({"query_embedding": embed_query(query), "document_embeddings": embed_documents(docs)})
