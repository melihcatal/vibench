from model_client import get_openai_client, get_embedding_model
from model_models import normalize_embedding


def output_embedding(text: str):
    client = get_openai_client()
    response = client.embeddings.create(model=get_embedding_model(), input=text)
    return normalize_embedding(response.data[0].embedding)
