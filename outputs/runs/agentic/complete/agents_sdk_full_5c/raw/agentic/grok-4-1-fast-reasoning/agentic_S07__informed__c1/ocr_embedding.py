import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
if client.api_key is None:
    raise ValueError("OPENAI_API_KEY not set")

def ocr_embedding(sections: list[str], model: str = "text-embedding-3-small") -> list[list[float]]:
    response = client.embeddings.create(
        input=sections,
        model=model,
    )
    return [embedding.embedding for embedding in response.data]