import os
from typing import Dict, List

from embeddings_client import DirectEmbeddingsClient
from embeddings_models import EmbeddingRequest, normalize_embedding_response


DEFAULT_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def embedding_job_summary(texts: List[str], model: str = DEFAULT_MODEL) -> Dict[str, object]:
    client = DirectEmbeddingsClient()
    response = client.embed(EmbeddingRequest(model=model, input=texts))
    normalized = normalize_embedding_response(response)
    vectors = normalized.embeddings or []
    dimensions = len(vectors[0]) if vectors else 0
    return {
        "count": len(vectors),
        "dimensions": dimensions,
        "model": model,
        "provider": "openai",
    }


if __name__ == "__main__":
    import json
    import sys

    payload = json.loads(sys.stdin.read() or "[]")
    print(json.dumps(embedding_job_summary(payload)))
