import os
from typing import List

from openai import OpenAI

from embeddings_models import EmbeddingRequest, normalize_embeddings


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def embed_texts(
    texts: List[str], model: str = "text-embedding-3-small"
) -> List[List[float]]:
    client = get_openai_client()
    request = EmbeddingRequest(inputs=texts, model=model)
    response = client.embeddings.create(model=request.model, input=list(request.inputs))
    return normalize_embeddings(response.model_dump()).embeddings
