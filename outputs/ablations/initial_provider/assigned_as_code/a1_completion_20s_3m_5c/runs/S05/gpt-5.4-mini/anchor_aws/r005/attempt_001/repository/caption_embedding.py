import os

from openai import OpenAI

from speech_models import normalize_text


def caption_embedding(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("api_key") or os.environ.get("OPENAI_API_KEY"))
    text = normalize_text(payload.get("text"))
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    embedding = response.data[0].embedding
    return {"text": text, "embedding": embedding, "model": "text-embedding-3-small"}
