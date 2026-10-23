from openai import OpenAI

from translation_client import get_client
from translation_models import normalize_text


def translation_memory_embedding(segment: str) -> list[float]:
    client: OpenAI = get_client()
    result = client.embeddings.create(
        model="text-embedding-3-small", input=normalize_text(segment)
    )
    return result.data[0].embedding
