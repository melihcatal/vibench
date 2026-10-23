import os

from openai import OpenAI


def platform_output_embedding(text: str) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return {
        "provider": "openai",
        "raw": response,
        "embedding": response.data[0].embedding,
        "model": "text-embedding-3-small",
    }
