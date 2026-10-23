import os
from embeddings_client import get_embed_client
from similarity_score import cosine_similarity

def embed_for_search(query: str, documents: list[str], model: str = 'text-embedding-3-large') -> list[tuple[int, float]]:
    """Embed a query and a list of document texts, then return ranked document indices by similarity.
    Provider: OpenAI (OpenAI Embeddings) – identifiable by the SDK import `openai` in `embeddings_client`.
    """
    client = get_embed_client()
    query_emb = client.create_embedding(model=model, input=[query])['data'][0]['embedding']
    doc_embs = []
    for doc in documents:
        emb = client.create_embedding(model=model, input=[doc])['data'][0]['embedding']
        doc_embs.append(emb)
    # Compute cosine similarities
    scores = [cosine_similarity(query_emb, d) for d in doc_embs]
    # Return (document_index, score) sorted descending
    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
    return ranked
