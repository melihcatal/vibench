from openai import OpenAI

from safety_client import default_embedding_model, get_client
from safety_models import EmbeddingResult


def moderation_reason_embedding(text: str) -> EmbeddingResult:
    client: OpenAI = get_client()
    response = client.embeddings.create(model=default_embedding_model(), input=text)
    return EmbeddingResult(vector=list(response.data[0].embedding))
