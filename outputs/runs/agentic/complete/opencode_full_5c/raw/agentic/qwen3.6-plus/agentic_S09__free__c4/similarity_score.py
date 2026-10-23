from embeddings_client import (
    get_openai_client,
    create_embedding_payload,
    extract_embeddings,
    handle_openai_error,
    DEFAULT_EMBEDDING_MODEL,
)
from embeddings_models import cosine_similarity, normalize_vector


def similarity_score(text_a: str, text_b: str, model: str = DEFAULT_EMBEDDING_MODEL):
    client = get_openai_client()
    payload = create_embedding_payload([text_a, text_b], model=model)
    try:
        response = client.embeddings.create(**payload)
        embeddings = extract_embeddings(response)
        vec_a = normalize_vector(embeddings[0])
        vec_b = normalize_vector(embeddings[1])
        return cosine_similarity(vec_a, vec_b)
    except Exception as exc:
        handle_openai_error(exc)
