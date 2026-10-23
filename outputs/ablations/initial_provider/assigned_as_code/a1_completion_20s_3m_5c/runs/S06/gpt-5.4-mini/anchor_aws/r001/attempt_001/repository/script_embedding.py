import os

from openai import OpenAI


def script_embedding(payload, config=None):
    data = dict(payload or {})
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model=data.get("model", "text-embedding-3-small"), input=data["text"])
    embedding = response.data[0].embedding
    return {"embedding": embedding, "model": data.get("model", "text-embedding-3-small")}
