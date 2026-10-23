from typing import List, Optional, Tuple
from openai import OpenAI
from embeddings_models import SearchResult, rank_documents_by_similarity
from embeddings_client import create_openai_client, DEFAULT_MODEL


def embed_for_search(
    query: str,
    documents: List[str],
    model: str = DEFAULT_MODEL,
    dimensions: Optional[int] = None,
    top_k: Optional[int] = None,
    api_key: Optional[str] = None,
) -> SearchResult:
    client = create_openai_client(api_key)
    all_inputs = [query] + documents
    payload = {
        "model": model,
        "input": all_inputs,
        "encoding_format": "float",
    }
    if dimensions is not None:
        payload["dimensions"] = dimensions
    response = client.embeddings.create(**payload)
    all_embeddings = [item.embedding for item in response.data]
    query_embedding = all_embeddings[0]
    document_embeddings = all_embeddings[1:]
    return rank_documents_by_similarity(
        query_embedding=query_embedding,
        document_embeddings=document_embeddings,
        documents=documents,
        top_k=top_k,
    )
