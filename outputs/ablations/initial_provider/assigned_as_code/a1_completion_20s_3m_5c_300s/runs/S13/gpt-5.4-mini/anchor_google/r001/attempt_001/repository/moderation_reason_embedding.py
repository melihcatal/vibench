import os

from openai import OpenAI


def moderation_reason_embedding(payload, config=None):
    client = OpenAI(api_key=(config or {}).get("api_key") or os.environ["OPENAI_API_KEY"])
    model = (config or {}).get("model", "text-embedding-3-small")
    response = client.embeddings.create(model=model, input=payload["text"])
    return {"embedding": response.data[0].embedding, "model": model}
