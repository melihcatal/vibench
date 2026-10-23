import os

from openai import OpenAI


def secret_audit_embedding(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("openai_api_key") or os.environ.get("OPENAI_API_KEY"))
    text = payload.get("notes", "")
    model = config.get("model", "text-embedding-3-small")
    response = client.embeddings.create(model=model, input=text)
    return {"embedding": response.data[0].embedding, "model": model}
