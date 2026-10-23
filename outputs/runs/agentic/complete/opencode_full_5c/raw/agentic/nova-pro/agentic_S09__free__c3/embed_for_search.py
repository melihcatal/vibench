import os

from embeddings_client import DirectEmbeddingsClient


def embed_for_search(query: str, documents: list) -> list:
    client = DirectEmbeddingsClient()
    query_embedding = client.embed_text(query).embeddings[0]
    document_embeddings = [client.embed_text(doc).embeddings[0] for doc in documents]
    scores = [
        DirectEmbeddingsClient.cosine_similarity(query_embedding, doc_embedding)
        for doc_embedding in document_embeddings
    ]
    sorted_documents = sorted(zip(documents, scores), key=lambda x: x[1], reverse=True)
    return [doc for doc, score in sorted_documents]
