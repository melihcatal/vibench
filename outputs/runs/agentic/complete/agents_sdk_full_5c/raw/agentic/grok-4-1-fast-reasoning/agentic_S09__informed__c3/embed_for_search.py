from typing import List, Tuple
from embeddings_client import get_client, EMBEDDING_MODEL
from embeddings_models import extract_embeddings, cosine_similarity

def embed_for_search(query: str, documents: list[str]) -> List[Tuple[str, float]]:
    client = get_client()
    all_texts = [query] + documents
    response = client.embeddings.create(
        input=all_texts,
        model=EMBEDDING_MODEL
    )
    embeddings = extract_embeddings(response)
    q_emb = embeddings[0]
    doc_embs = embeddings[1:]
    scores = [cosine_similarity(q_emb, doc_emb) for doc_emb in doc_embs]
    results = list(zip(documents, scores))
    results.sort(key=lambda x: x[1], reverse=True)
    return results