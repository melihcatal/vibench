import os
from typing import List

from openai import OpenAI

from embeddings_models import EmbeddingRequest, extract_embeddings

OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def get_client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def embed_texts(texts: List[str]) -> List[List[float]]:
    client = get_client()
    req = EmbeddingRequest(texts=texts)
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=req.texts)
    return extract_embeddings(response)
