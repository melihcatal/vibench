from typing import List, Tuple
from embeddings_client import get_openai_client
from embeddings_models import EmbeddingRequest, normalize_embedding


def embed_for_search(
    query: str, documents: List[str]
) -> Tuple[List[float], List[List[float]]]:
    """
    Embeds a query and a list of documents for semantic search using OpenAI.
    Returns the normalized query embedding and a list of normalized document embeddings.
    """
    client = get_openai_client()
    all_texts = [query] + documents
    request_data = EmbeddingRequest(input=all_texts)
    response = client.embeddings.create(
        input=request_data.input, model=request_data.model
    )

    query_embedding = normalize_embedding(response.data[0].embedding)
    document_embeddings = [
        normalize_embedding(item.embedding) for item in response.data[1:]
    ]

    return query_embedding, document_embeddings
