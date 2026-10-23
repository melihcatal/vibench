from embeddings_client import get_client, get_model


def embed_for_search(payload, config=None):
    config = config or {}
    with get_client(config) as client:
        query_response = client.models.embed_content(model=get_model(config), contents=payload["query"])
        doc_response = client.models.embed_content(model=get_model(config), contents=payload["documents"])
    return {
        "query_embedding": list(query_response.embeddings[0].values),
        "document_embeddings": [list(item.values) for item in doc_response.embeddings],
    }
