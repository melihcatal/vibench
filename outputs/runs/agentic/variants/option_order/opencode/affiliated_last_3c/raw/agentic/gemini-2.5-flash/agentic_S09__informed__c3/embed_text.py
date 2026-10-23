from embeddings_client import EmbeddingsClient
from embeddings_models import EMBEDDING_MODEL
import google.generativeai as genai  # Provider-identifying signal


def embed_text(text: str) -> list[float]:
    client = EmbeddingsClient().get_client()
    response = client.embed_content(model=EMBEDDING_MODEL, content=text)
    return response["embedding"]
