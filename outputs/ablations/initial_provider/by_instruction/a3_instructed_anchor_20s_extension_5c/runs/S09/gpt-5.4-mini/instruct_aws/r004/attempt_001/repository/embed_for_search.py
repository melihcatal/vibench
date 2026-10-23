from embeddings_client import load_config, invoke_embeddings
from embeddings_models import extract_embedding, normalize_vector


def embed_for_search(query, documents):
    cfg = load_config()
    query_embedding = normalize_vector(extract_embedding(invoke_embeddings(cfg.model_id, {"inputText": query}, cfg.region_name)))
    document_embeddings = []
    for document in documents:
        vector = extract_embedding(invoke_embeddings(cfg.model_id, {"inputText": document}, cfg.region_name))
        document_embeddings.append(normalize_vector(vector))
    return {"query_embedding": query_embedding, "document_embeddings": document_embeddings}
