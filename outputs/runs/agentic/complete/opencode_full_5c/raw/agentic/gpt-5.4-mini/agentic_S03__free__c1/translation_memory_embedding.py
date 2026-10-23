from openai import OpenAI

from translation_client import get_client


EMBEDDING_MODEL = "text-embedding-3-small"


def translation_memory_embedding(text: str):
    client: OpenAI = get_client()
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return response.data[0].embedding if response.data else []
