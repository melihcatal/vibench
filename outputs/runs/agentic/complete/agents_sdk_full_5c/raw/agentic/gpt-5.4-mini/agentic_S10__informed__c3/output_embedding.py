import os
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-large")


def embed_output(text: str) -> list[float]:
    client = OpenAI(api_key=OPENAI_API_KEY, base_url=os.getenv("OPENAI_BASE_URL"))
    response = client.embeddings.create(model=EMBED_MODEL, input=text)
    return response.data[0].embedding
