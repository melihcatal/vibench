import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def embed_script(script: str) -> list[float]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=script,
    )
    return response.data[0].embedding
