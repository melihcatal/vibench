from embeddings_client import create_client, get_model_name
from embeddings_models import cosine_similarity


def similarity_score(text_a: str, text_b: str) -> float:
    client = create_client()
    model = get_model_name()
    embeddings = client.embeddings.create(model=model, input=[text_a, text_b]).data
    return cosine_similarity(embeddings[0].embedding, embeddings[1].embedding)
