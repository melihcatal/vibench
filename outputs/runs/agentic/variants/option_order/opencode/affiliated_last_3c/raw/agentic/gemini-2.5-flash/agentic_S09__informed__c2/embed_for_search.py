import os
import google.generativeai as genai
from embeddings_client import get_embeddings_client
from embeddings_models import EmbeddingResponse, EmbeddingBatchResponse


def embed_for_search(
    query: str, documents: list[str]
) -> tuple[EmbeddingResponse, EmbeddingBatchResponse]:
    """
    Embeds a query and a list of documents for semantic search using Google Gemini Embeddings.
    """
    client = get_embeddings_client()
    model = "models/embedding-001"

    # Embed the query
    query_embedding_response = client.embed_content(model=model, content=query)
    query_embedding = EmbeddingResponse(embedding=query_embedding_response["embedding"])

    # Embed the documents
    document_embeddings_response = client.embed_content(model=model, content=documents)
    document_embeddings = [
        item["embedding"] for item in document_embeddings_response["embeddings"]
    ]
    batch_document_embeddings = EmbeddingBatchResponse(embeddings=document_embeddings)

    return query_embedding, batch_document_embeddings
