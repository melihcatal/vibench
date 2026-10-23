from embeddings_client import get_client, load_config
from embeddings_models import normalize_vector


def embed_for_search(query, documents):
    client = get_client()
    config = load_config()
    query_response = client.models.embed_content(model=config.model, contents=query)
    document_response = client.models.embed_content(model=config.model, contents=list(documents))
    return {
        "query_embedding": normalize_vector(query_response.embeddings[0].values),
        "document_embeddings": [normalize_vector(item.values) for item in document_response.embeddings],
    }
