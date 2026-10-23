from embeddings_client import create_client, invoke_embedding
from embeddings_models import normalize_text, normalize_texts


def embed_for_search(payload, config=None):
    client, cfg = create_client(config)
    query = normalize_text(payload["query"])
    documents = normalize_texts(payload["documents"])
    return {
        "query_embedding": invoke_embedding(client, cfg["model_id"], query),
        "document_embeddings": [invoke_embedding(client, cfg["model_id"], document) for document in documents],
    }
