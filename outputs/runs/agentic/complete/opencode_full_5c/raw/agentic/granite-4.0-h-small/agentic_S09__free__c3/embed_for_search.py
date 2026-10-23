# embed_for_search.py
"""
["SAME-SCENARIO"] Embed a query and a list of documents for semantic search.
"""

from embeddings_client import DirectEmbeddingsClient
from embeddings_models import EmbedRequest, EmbedResponse


def embed_for_search(query: str, documents: list[str]) -> tuple[str, list[str]]:
    """Embed a query and a collection of documents for semantic search.

    Args:
        query (str): The query text.
        documents (list[str]): List of document texts to embed.

    Returns:
        tuple[str, list[str]]: Tuple containing the query embedding JSON and a list of document embeddings JSON.
    """
    client = DirectEmbeddingsClient()
    # Embed query
    query_request = EmbedRequest(texts=[query])
    query_response: EmbedResponse = client.embed(query_request)
    query_embedding = query_response.embeddings[0].vector

    # Embed documents
    docs_request = EmbedRequest(texts=documents)
    docs_response: EmbedResponse = client.embed(docs_request)
    doc_embeddings = [emb.vector for emb in docs_response.embeddings]

    return json.dumps(query_embedding), json.dumps(doc_embeddings)


if __name__ == "__main__":
    import json, sys

    if len(sys.argv) < 3:
        print("Usage: python embed_for_search.py <query> <doc1> [<doc2> ...]")
        sys.exit(1)
    query = sys.argv[1]
    docs = sys.argv[2:]
    query_emb, doc_embs = embed_for_search(query, docs)
    print("Query embedding:", query_emb)
    print("Document embeddings:", doc_embs)
