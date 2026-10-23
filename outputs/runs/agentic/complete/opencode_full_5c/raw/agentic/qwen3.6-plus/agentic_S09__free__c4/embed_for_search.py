from embeddings_client import (
    get_openai_client,
    create_embedding_payload,
    extract_embeddings,
    handle_openai_error,
    DEFAULT_EMBEDDING_MODEL,
)
from embeddings_models import build_search_results, normalize_vector


def embed_for_search(query: str, documents: list, model: str = DEFAULT_EMBEDDING_MODEL):
    client = get_openai_client()
    all_texts = [query] + documents
    payload = create_embedding_payload(all_texts, model=model)
    try:
        response = client.embeddings.create(**payload)
        embeddings = extract_embeddings(response)
        query_embedding = normalize_vector(embeddings[0])
        doc_embeddings = [normalize_vector(e) for e in embeddings[1:]]
        return build_search_results(query_embedding, doc_embeddings, documents)
    except Exception as exc:
        handle_openai_error(exc)
