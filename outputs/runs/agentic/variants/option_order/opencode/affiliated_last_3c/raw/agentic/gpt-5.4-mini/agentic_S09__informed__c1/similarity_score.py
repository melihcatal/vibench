from embeddings_client import get_client, get_embedding_model, normalize_texts
from embeddings_models import cosine_similarity


def similarity_score(text_a: str, text_b: str):
    client = get_client()
    response = client.embeddings.create(
        model=get_embedding_model(), input=normalize_texts([text_a, text_b])
    )
    return cosine_similarity(response.data[0].embedding, response.data[1].embedding)
