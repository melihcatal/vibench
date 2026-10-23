import os
from typing import List, Dict
import google.generativeai as genai

from embeddings_client import get_gemini_embedding_model
from embeddings_models import EmbeddingResponse

def embed_for_search(query: str, documents: List[str], api_key: str = None) -> Dict[str, List[List[float]]]:
    """
    Embeds a query and a list of documents for semantic search using Google's Gemini embedding model.
    Returns a dictionary with 'query_embedding' and 'document_embeddings'.
    """
    model = get_gemini_embedding_model(api_key)

    # Embed the query
    query_response = genai.embed_content(model=model, content=query, task_type="RETRIEVAL_QUERY")
    query_embedding = EmbeddingResponse.from_genai_response(query_response).embeddings[0]

    # Embed the documents
    document_responses = genai.embed_content(model=model, content=documents, task_type="RETRIEVAL_DOCUMENT")
    document_embeddings = EmbeddingResponse.from_genai_response(document_responses).embeddings

    return {
        "query_embedding": query_embedding,
        "document_embeddings": document_embeddings,
    }
