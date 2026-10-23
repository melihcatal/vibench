from google import genai

from embeddings_client import get_client, get_model
from embeddings_models import extract_embeddings, normalize_texts


def embed_batch(payload, config=None):
    config = config or {}
    texts = normalize_texts(payload)
    model = get_model(config)
    with get_client(config) as client:
        response = client.models.embed_content(model=model, contents=texts)
    return {"embeddings": extract_embeddings(response)}
