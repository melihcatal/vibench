from embeddings_client import get_embeddings_client
from embeddings_models import normalize_embedding_response


def embed_for_search(payload, config=None):
    client = get_embeddings_client(config)
    query_embedding = client.models.embed_content(model="gemini-embedding-001", contents=payload["query"])[0]
    document_embeddings = client.models.embed_content(model="gemini-embedding-001", contents=payload["documents"])
    normalized_query_embedding = normalize_embedding_response(query_embedding)
    normalized_document_embeddings = [normalize_embedding_response(embedding) for embedding in document_embeddings]
    return {"query_embedding": normalized_query_embedding, "document_embeddings": normalized_document_embeddings}