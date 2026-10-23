import os
from statistics import mean
from typing import Dict, List

from embeddings_client import create_embeddings_client
from embeddings_models import BatchEmbeddingRequest, extract_embeddings, normalize_texts


def summarize_embedding_job(texts: List[str], model: str | None = None) -> Dict[str, float]:
    client = create_embeddings_client()
    embedding_model = model or os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    embeddings = extract_embeddings(client.create_embeddings(BatchEmbeddingRequest(inputs=normalize_texts(texts), model=embedding_model)))
    lengths = [len(vec) for vec in embeddings]
    return {"count": float(len(embeddings)), "avg_dimensions": float(mean(lengths)) if lengths else 0.0, "max_dimensions": float(max(lengths)) if lengths else 0.0}
