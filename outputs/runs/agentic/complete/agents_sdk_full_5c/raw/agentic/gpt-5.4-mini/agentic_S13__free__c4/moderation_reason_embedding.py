from openai import OpenAI

from safety_client import get_openai_client


client: OpenAI = get_openai_client()
EMBEDDING_MODEL = "text-embedding-3-small"


def moderation_reason_embedding(rationale: str) -> list[float]:
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=rationale)
    return response.data[0].embedding
