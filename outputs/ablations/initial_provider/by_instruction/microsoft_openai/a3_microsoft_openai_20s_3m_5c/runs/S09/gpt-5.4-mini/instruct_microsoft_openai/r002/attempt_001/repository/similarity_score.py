from embeddings_client import get_client, embeddings_model
from embeddings_models import cosine_similarity


def similarity_score(text_a: str, text_b: str) -> float:
    client = get_client()
    response = client.embeddings.create(model=embeddings_model(), input=[text_a, text_b])
    return cosine_similarity(response.data[0].embedding, response.data[1].embedding)
