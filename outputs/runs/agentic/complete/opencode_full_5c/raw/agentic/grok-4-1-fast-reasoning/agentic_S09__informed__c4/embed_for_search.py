from typing import List, Dict
from embeddings_client import get_embeddings_client
from embeddings_models import prepare_input, parse_embeddings


def embed_for_search(query: str, documents: List[str]) -> Dict[str, List[List[float]]]:
    client = get_embeddings_client()
    all_texts = prepare_input(query) + documents
    response = client.embeddings.create(model="text-embedding-3-small", input=all_texts)
    embeddings = parse_embeddings(response)
    query_emb = embeddings[0]
    doc_embs = embeddings[1:]
    return {"query_embedding": [query_emb], "document_embeddings": doc_embs}
