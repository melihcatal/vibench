# embed_for_search.py
import os
from embeddings_client import DirectEmbeddingsClient
from embeddings_models import check_response
from similarity_score import cosine_similarity

def embed_for_search(query: str, corpus: list[str]):
    """Embed a query and a corpus, then return similarity scores.

    Args:
        query (str): search query.
        corpus (list[str]): list of document strings.

    Returns:
        list[tuple[str, float]]: ranked (document, similarity) pairs.
    """
    client = DirectEmbeddingsClient()
    # Embed query
    query_resp = client.create_embedding(
        input=query,
        model="text-embedding-ada-002"
    )
    check_response(query_resp)
    query_emb = query_resp['data'][0]['embedding']

    # Embed corpus
    corpus_resp = client.create_embedding(
        input=corpus,
        model="text-embedding-ada-002"
    )
    check_response(corpus_resp)
    corpus_embs = [item['embedding'] for item in corpus_resp['data']]

    # Compute similarities
    scored = [(doc, cosine_similarity(query_emb, emb))
              for doc, emb in zip(corpus, corpus_embs)]
    # Sort descending by similarity
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored
