from embeddings_client import get_openai_client, load_config
from embeddings_models import SearchDocument, cosine_similarity, normalize_text


def embed_for_search(query: str, documents):
    cfg = load_config()
    client = get_openai_client()
    query_vec = client.embeddings.create(model=cfg.model, input=normalize_text(query)).data[0].embedding
    doc_texts = [normalize_text(doc["text"] if isinstance(doc, dict) else doc.text) for doc in documents]
    doc_embeddings = client.embeddings.create(model=cfg.model, input=doc_texts).data
    scored = []
    for idx, item in enumerate(doc_embeddings):
        doc = documents[idx]
        doc_id = doc["id"] if isinstance(doc, dict) else doc.id
        doc_text = doc["text"] if isinstance(doc, dict) else doc.text
        score = cosine_similarity(query_vec, item.embedding)
        scored.append(SearchDocument(id=str(doc_id), text=doc_text, score=score, embedding=item.embedding))
    scored.sort(key=lambda d: d.score or 0.0, reverse=True)
    return {"query_embedding": query_vec, "documents": scored}
