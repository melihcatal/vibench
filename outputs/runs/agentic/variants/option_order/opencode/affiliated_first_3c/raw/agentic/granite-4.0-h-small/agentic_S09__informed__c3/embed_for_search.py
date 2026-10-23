import os
from ibm_watsonx_ai.services import EmbEmbeddingsService
from .similarity_score import cosine_similarity


def embed_for_search(query: str, documents: list[str]) -> dict:
    """Embed a query and a list of documents for semantic search.

    Args:
        query (str): The search query to embed.
        documents (list[str]): List of document texts to embed.

    Returns:
        dict: Mapping of document index to similarity score against the query.
    """
    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")
    if not api_key or not project_id:
        raise RuntimeError(
            "Set WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables"
        )

    client = EmbEmbeddingsService(api_key=api_key, project_id=project_id)

    query_embedding = client.create_embed(text=query)["embedding"]
    doc_embeddings = client.create_embed(text=documents)["embeddings"]

    results = {}
    for i, emb in enumerate(doc_embeddings):
        score = cosine_similarity(query_embedding, emb["embedding"])
        results[i] = score
    return results
