import os
from pathlib import Path
from typing import List, Optional

# Configuration values (set as environment variables)
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")


# Helper:
def _prepare_payload(texts: List[str], model_id: str) -> dict:
    """Create IBM Watsonx embeddings API payload.","""
    return {"input": texts, "model": model_id}


def retrieve_and_search(
    query: str, corpus: List[str], model_id: Optional[str] = None, max_results: int = 5
) -> List[str]:
    """Retrieve top similar documents for a single query using cosine similarity.","""
    model_id = model_id if model_id else "embed-ada-002"
    client = create_client()
    # 1) embed corpus
    payload_corpus = _prepare_payload(corpus, model_id=model_id)
    response_corpus = client.create_embeddings(payload_corpus)  # type: ignore
    # Assume response is list of dicts with 'embeddings' list
    corpus_vecs = [_["embeddings"][0] for _ in response_corpus]
    # 2) embed query
    payload_q = _prepare_payload([query], model_id=model_id)
    response_q = client.create_embeddings(payload_q)  # type: ignore
    query_vec = response_q[0]["embeddings"][0]
    # 3) compute similarities (cosine)
    sims = [cosine_similarity(query_vec, c) for c in corpus_vecs]
    # 4) pick top results
    top_indices = sorted(range(len(sims)), key=lambda i: sims[i], reverse=True)[
        :max_results
    ]
    return [corpus[i] for i in top_indices]


# -----------------------------------------------------------------------------
