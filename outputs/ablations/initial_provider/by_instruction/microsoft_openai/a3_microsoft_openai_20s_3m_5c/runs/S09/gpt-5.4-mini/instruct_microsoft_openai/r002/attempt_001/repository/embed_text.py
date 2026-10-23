from embeddings_client import get_client, embeddings_model
from embeddings_models import normalize_vector


def embed_text(text: str):
    response = get_client().embeddings.create(model=embeddings_model(), input=text)
    return normalize_vector(response.data[0].embedding)
