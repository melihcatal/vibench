from embeddings_client import embed_inputs, normalize_text
from embeddings_models import EmbeddingVector, vector_from_response_item


def embed_for_search(query: str, documents):
    normalized_query = normalize_text(query)
    normalized_documents = [normalize_text(document) for document in documents]
    response = embed_inputs([normalized_query, *normalized_documents])
    query_embedding = EmbeddingVector(text=normalized_query, vector=vector_from_response_item(response.data[0]))
    document_embeddings = [EmbeddingVector(text=text, vector=vector_from_response_item(item)) for text, item in zip(normalized_documents, response.data[1:])]
    return query_embedding, document_embeddings
