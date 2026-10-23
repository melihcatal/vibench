from embeddings_client import create_client, get_model
from embeddings_models import extract_embeddings, normalize_texts


def embed_for_search(payload, config=None):
    config = config or {}
    query = payload["query"]
    documents = normalize_texts({"texts": payload["documents"]})
    with create_client(config) as client:
        query_response = client.models.embed_content(model=get_model(config), contents=query)
        docs_response = client.models.embed_content(model=get_model(config), contents=documents)
    return {"query_embedding": extract_embeddings(query_response)[0], "document_embeddings": extract_embeddings(docs_response)}
