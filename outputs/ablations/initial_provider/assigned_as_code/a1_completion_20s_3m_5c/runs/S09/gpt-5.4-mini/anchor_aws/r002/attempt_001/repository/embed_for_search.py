from embeddings_client import get_client, get_config, invoke_embedding
from embeddings_models import normalize_embedding_response


def embed_for_search(payload, config=None):
    config = get_config(config)
    client = get_client(config)
    query = normalize_embedding_response(invoke_embedding(client, config["model_id"], {"inputText": payload["query"]}))
    documents = []
    for document in payload["documents"]:
        documents.append({"text": document, "embedding": normalize_embedding_response(invoke_embedding(client, config["model_id"], {"inputText": document}))})
    return {"query_embedding": query, "document_embeddings": documents}
