import os
import cohere

from embeddings_client import get_embedding_client, DEFAULT_MODEL
from embeddings_models import SearchEmbeddingRequest, normalize_embedding_result


def embed_for_search(query: str, documents):
    client = get_embedding_client()
    request = SearchEmbeddingRequest(query=query, documents=documents, model=os.getenv("COHERE_EMBED_MODEL", DEFAULT_MODEL))
    query_response = client.embed(texts=[request.query], model=request.model, input_type="search_query")
    doc_response = client.embed(texts=request.documents, model=request.model, input_type="search_document")
    return {
        "query_embedding": normalize_embedding_result(query_response, single_text=request.query)[0],
        "document_embeddings": normalize_embedding_result(doc_response),
    }

