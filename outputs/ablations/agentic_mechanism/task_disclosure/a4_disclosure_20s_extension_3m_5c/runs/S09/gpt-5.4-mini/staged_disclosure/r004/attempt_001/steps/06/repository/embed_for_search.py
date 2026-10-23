import os
from typing import Iterable, List

from openai import OpenAI


def embed_for_search(query: str, documents: Iterable[str]) -> dict:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    texts: List[str] = [query, *list(documents)]
    response = client.embeddings.create(model="text-embedding-3-small", input=texts)
    vectors = [item.embedding for item in response.data]
    return {"query_embedding": vectors[0], "document_embeddings": vectors[1:]}


if __name__ == "__main__":
    raise SystemExit(0)
