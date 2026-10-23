from embeddings_client import get_client
from embeddings_models import MODEL_EMBED, normalize_text

def embed_text(text: str) -> list[float]:
    client = get_client()
    response = client.embeddings.create(
        model=MODEL_EMBED,
        input=normalize_text(text)
    )
    return response.data[0].embedding