import os

from openai import OpenAI


def embed_output(text: str, model: str | None = None) -> list[float]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL"))
    response = client.embeddings.create(model=model or os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large"), input=text)
    return list(response.data[0].embedding)
