import os
from typing import Any, Dict, List

from embeddings_client import DirectEmbeddingsClient
from embeddings_models import EmbeddingRequest, normalize_embedding_response


DEFAULT_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def embed_text(text: str, model: str = DEFAULT_MODEL) -> List[float]:
    client = DirectEmbeddingsClient()
    request = EmbeddingRequest(model=model, input=text)
    response = client.embed(request)
    normalized = normalize_embedding_response(response)
    return normalized.embedding


if __name__ == "__main__":
    import json
    import sys

    text = sys.stdin.read().strip()
    result = embed_text(text)
    print(json.dumps({"embedding": result}))
