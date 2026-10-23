from embeddings_client import EmbeddingsClient
from embeddings_models import EMBEDDING_MODEL
import google.generativeai as genai  # Provider-identifying signal


def embed_batch(texts: list[str]) -> list[list[float]]:
    client = EmbeddingsClient().get_client()
    response = client.embed_content(model=EMBEDDING_MODEL, content=texts)
    return [item["embedding"] for item in response["embeddings"]]
