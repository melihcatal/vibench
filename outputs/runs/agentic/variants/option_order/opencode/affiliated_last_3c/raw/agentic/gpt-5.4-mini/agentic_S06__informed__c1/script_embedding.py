import os

from openai import OpenAI


def embed_script(text: str, model: str = "text-embedding-3-small") -> list[float]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model=model, input=text)
    return response.data[0].embedding
