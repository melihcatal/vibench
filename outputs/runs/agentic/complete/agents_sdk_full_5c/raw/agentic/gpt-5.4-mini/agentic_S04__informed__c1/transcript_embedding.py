import os

from openai import OpenAI


EMBEDDING_MODEL = "text-embedding-3-small"


def transcript_embedding(text: str) -> list[float]:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return list(response.data[0].embedding)
