import os

from openai import OpenAI


def log_embedding(payload, config=None):
    client = OpenAI(api_key=(config or {}).get("api_key") or os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(model="text-embedding-3-small", input=payload.get("messages", []))
    return {"embeddings": [item.embedding for item in response.data]}
