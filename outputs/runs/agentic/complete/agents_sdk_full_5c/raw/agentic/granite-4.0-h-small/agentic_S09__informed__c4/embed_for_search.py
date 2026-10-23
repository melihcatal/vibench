# embed_for_search.py

from embeddings_client import get_client
from embeddings_models import normalize_embedding

def embed_for_search(query: str, docs: list[str]) -> tuple[list[float], list[list[float]]]:
    """Embed a query and a list of documents for semantic search.

    Args:
        query (str): Query text.
        docs (List[str]): List of document texts.

    Returns:
        Tuple[List[float], List[List[float]]]: Embedded query and list of embedded documents.
    """
    client = get_client()
    query_res = client.embeddings.create(
        model="text-embedding-ada-002",  # OpenAI model identifier (example)
        input=query,
    )
    query_embedding = normalize_embedding(query_res["data"][0]["embedding"])

    doc_embeddings = []
    for doc in docs:
        resp = client.embeddings.create(
            model="text-embedding-ada-002",
            input=doc,
        )
        doc_embeddings.append(normalize_embedding(resp["data"][0]["embedding"]))
    return query_embedding, doc_embeddings
