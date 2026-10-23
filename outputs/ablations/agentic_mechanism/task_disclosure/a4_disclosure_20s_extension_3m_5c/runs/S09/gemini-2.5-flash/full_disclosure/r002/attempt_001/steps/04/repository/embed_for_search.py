from typing import List

from vertexai.language_models import TextEmbeddingModel


def embed_for_search(query: str, documents: List[str]):
    """Embeds a query and documents for semantic search using Vertex AI."""
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")

    # Embed the query
    query_embedding = model.get_embeddings([query])[0].values

    # Embed the documents
    document_embeddings = [
        embedding.values for embedding in model.get_embeddings(documents)
    ]

    return query_embedding, document_embeddings
