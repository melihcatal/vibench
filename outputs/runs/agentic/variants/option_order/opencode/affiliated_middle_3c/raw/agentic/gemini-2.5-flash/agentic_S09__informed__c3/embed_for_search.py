import google.generativeai as genai
from embeddings_client import configure_embeddings_client
from embeddings_models import normalize_embedding_response
from typing import List


def embed_query(query: str) -> list[float]:
    configure_embeddings_client()
    response = genai.embed_content(
        model="embedding-001", content=query, task_type="RETRIEVAL_QUERY"
    )
    return normalize_embedding_response(response)


def embed_documents(documents: List[str]) -> List[List[float]]:
    configure_embeddings_client()
    responses = genai.embed_content(
        model="embedding-001", content=documents, task_type="RETRIEVAL_DOCUMENT"
    )
    doc_embeddings = [
        normalize_embedding_response(res) for res in responses["embeddings"]
    ]
    return doc_embeddings
