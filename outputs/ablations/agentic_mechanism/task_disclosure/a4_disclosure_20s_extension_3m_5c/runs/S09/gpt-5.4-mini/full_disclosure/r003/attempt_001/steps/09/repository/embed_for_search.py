import os
from typing import List, Dict, Any

from openai import OpenAI


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def embed_for_search(query: str, documents: List[str], model: str = "text-embedding-3-small") -> Dict[str, Any]:
    client = _client()
    inputs = [query] + list(documents)
    response = client.embeddings.create(model=model, input=inputs)
    vectors = [item.embedding for item in response.data]
    return {"query_embedding": vectors[0], "document_embeddings": vectors[1:], "model": model}
