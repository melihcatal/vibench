import os
from openai import OpenAI

_PROVIDER_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def translation_memory_embedding(text: str) -> list:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) if os.getenv("OPENAI_API_KEY") else OpenAI()
    response = client.embeddings.create(model=_PROVIDER_MODEL, input=text)
    return response.data[0].embedding
