from typing import List, Tuple
from embeddings_client import get_client
from embeddings_models import parse_embeddings


def embed_for_search(
    query: str, documents: List[str]
) -> Tuple[List[float], List[List[float]]]:
    client = get_client()
    all_texts = [query] + documents
    response = client.embeddings.create(input=all_texts, model="text-embedding-3-small")
    embeddings = parse_embeddings(response)
    query_emb = embeddings[0]
    doc_embs = embeddings[1:]
    return query_emb, doc_embs
