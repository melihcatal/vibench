import os
from typing import List, Tuple, Dict, Any
from openai import OpenAI
import numpy as np


def embed_for_search(
    query: str, documents: List[str], model: str = "text-embedding-3-small"
) -> Tuple[List[float], List[List[float]], List[float]]:
    """
    Embed a query and documents for semantic search using OpenAI embeddings.

    Args:
        query: The search query string
        documents: List of document strings to search against
        model: The OpenAI embedding model to use (default: text-embedding-3-small)

    Returns:
        Tuple containing:
        - query_embedding: Embedding vector for the query
        - document_embeddings: List of embedding vectors for each document
        - similarity_scores: Cosine similarity scores between query and each document
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    # Embed query
    query_response = client.embeddings.create(
        model=model, input=query, encoding_format="float"
    )
    query_embedding = query_response.data[0].embedding

    # Embed documents
    doc_response = client.embeddings.create(
        model=model, input=documents, encoding_format="float"
    )
    document_embeddings = [item.embedding for item in doc_response.data]

    # Compute similarity scores
    query_vec = np.array(query_embedding)
    similarity_scores = []

    for doc_embedding in document_embeddings:
        doc_vec = np.array(doc_embedding)
        dot_product = np.dot(query_vec, doc_vec)
        norm_query = np.linalg.norm(query_vec)
        norm_doc = np.linalg.norm(doc_vec)

        if norm_query == 0 or norm_doc == 0:
            similarity = 0.0
        else:
            similarity = float(dot_product / (norm_query * norm_doc))

        similarity_scores.append(similarity)

    return query_embedding, document_embeddings, similarity_scores
