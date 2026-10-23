from embeddings_client import client
from embeddings_models import SearchRequest, SearchEmbeddingResponse


def embed_for_search(request: SearchRequest) -> SearchEmbeddingResponse:
    query_response = client.embeddings.create(
        input=request.query, model="text-embedding-3-small"
    )
    query_embedding = query_response.data[0].embedding

    doc_response = client.embeddings.create(
        input=request.documents, model="text-embedding-3-small"
    )
    document_embeddings = [item.embedding for item in doc_response.data]

    return SearchEmbeddingResponse(
        query_embedding=query_embedding, document_embeddings=document_embeddings
    )
