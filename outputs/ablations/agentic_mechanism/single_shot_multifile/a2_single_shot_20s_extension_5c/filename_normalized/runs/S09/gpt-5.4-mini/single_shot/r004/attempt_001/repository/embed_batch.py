import os
from typing import List

from embeddings_client import DirectEmbeddingsClient
from embeddings_models import EmbeddingRequest, normalize_embedding_response


DEFAULT_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def embed_batch(texts: List[str], model: str = DEFAULT_MODEL) -> List[List[float]]:
    client = DirectEmbeddingsClient()
    request = EmbeddingRequest(model=model, input=texts)
    response = client.embed(request)
    normalized = normalize_embedding_response(response)
    return normalized.embeddings


if __name__ == "__main__":
    import json
    import sys

    payload = json.loads(sys.stdin.read() or "[]")
    result = embed_batch(payload)
    print(json.dumps({"embeddings": result}))
