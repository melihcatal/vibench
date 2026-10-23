import os
from openai import OpenAI


def embed_translated_segment(text: str) -> list[float]:
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY required")
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    embedding_response = client.embeddings.create(
        input=text, model="text-embedding-3-small"
    )
    return embedding_response.data[0].embedding
