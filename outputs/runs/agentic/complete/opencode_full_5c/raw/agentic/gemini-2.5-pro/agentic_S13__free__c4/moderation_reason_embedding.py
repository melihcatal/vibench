from safety_client import get_openai_client
from safety_models import EmbeddingResult


def embed_moderation_reason(reason_text: str) -> EmbeddingResult:
    client = get_openai_client()

    response = client.embeddings.create(
        input=[reason_text], model="text-embedding-3-small"
    )

    embedding = response.data[0].embedding

    return EmbeddingResult(text=reason_text, embedding=embedding)
