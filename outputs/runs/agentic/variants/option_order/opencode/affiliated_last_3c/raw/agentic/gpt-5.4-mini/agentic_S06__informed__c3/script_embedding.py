import os

from openai import OpenAI


def embed_script(text: str, model: str = "text-embedding-3-small") -> list[float]:
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY is required")
    client = OpenAI()
    response = client.embeddings.create(model=model, input=text)
    return response.data[0].embedding
