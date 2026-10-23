import os
from embeddings_client import DirectEmbeddingsConfig

# Configuration
config = DirectEmbeddingsConfig(
    service="DashScope",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="text-embedding-ada-002",
)


def embed_for_search(
    query: str, documents: List[str]
) -> tuple[list[float], dict[str, list[float]]]:
    """Embed a query and a list of documents for semantic search using DashScope.

    Args:
        query (str): The search query text.
        documents (List[str]): List of document texts to embed.

    Returns:
        tuple:
            - list[float]: Embedding vector for the query.
            - dict[str, list[float]]: Mapping of document IDs to their embedding vectors.
    """
    client = config.get_client()
    # Embed query
    query_emb = client.embeddings.create(model=config.model, input=query)["embedding"]

    # Embed documents; assume documents have an 'id' field in metadata
    doc_embeddings = {}
    for doc in documents:
        # Assuming each doc is a dict with 'id' and 'text' keys
        doc_text = doc["text"] if isinstance(doc, dict) else doc
        emb = client.embeddings.create(model=config.model, input=doc_text)["embedding"]
        doc_embeddings[doc["id"]] = emb
    return query_emb, doc_embeddings
