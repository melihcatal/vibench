import os
from typing import Dict, List

from embeddings_client import DirectEmbeddingsClient
from embeddings_models import EmbeddingRequest, normalize_embedding_response, cosine_similarity


DEFAULT_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def embed_for_search(query: str, documents: List[str], model: str = DEFAULT_MODEL) -> Dict[str, object]:
    client = DirectEmbeddingsClient()
    query_resp = client.embed(EmbeddingRequest(model=model, input=query))
    doc_resp = client.embed(EmbeddingRequest(model=model, input=documents))
    query_vec = normalize_embedding_response(query_resp).embedding
    doc_vecs = normalize_embedding_response(doc_resp).embeddings
    scored = [
        {"document": doc, "score": cosine_similarity(query_vec, vec)}
        for doc, vec in zip(documents, doc_vecs)
    ]
    scored.sort(key=lambda item: item["score"], reverse=True)
    return {"query_embedding": query_vec, "results": scored}


if __name__ == "__main__":
    import json
    import sys

    payload = json.loads(sys.stdin.read())
    print(json.dumps(embed_for_search(payload["query"], payload["documents"])))
