import os
from typing import Dict, List

from embeddings_client import create_embeddings_client
from embeddings_models import BatchEmbeddingRequest, EmbeddingRequest, extract_embeddings, extract_single_embedding, normalize_text, normalize_texts


def embed_for_search(query: str, documents: List[str], model: str | None = None) -> Dict[str, List[float] | List[List[float]]]:
    client = create_embeddings_client()
    embedding_model = model or os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    query_vec = extract_single_embedding(client.create_embedding(EmbeddingRequest(input=normalize_text(query), model=embedding_model)))
    doc_vecs = extract_embeddings(client.create_embeddings(BatchEmbeddingRequest(inputs=normalize_texts(documents), model=embedding_model)))
    return {"query_embedding": query_vec, "document_embeddings": doc_vecs}
