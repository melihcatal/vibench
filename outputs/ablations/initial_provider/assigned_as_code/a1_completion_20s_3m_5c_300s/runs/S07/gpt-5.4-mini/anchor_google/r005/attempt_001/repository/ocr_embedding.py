import os
from openai import OpenAI


def ocr_embedding(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("api_key") or os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(model=config.get("model_id", "text-embedding-3-small"), input=payload["text"])
    return {"embedding": response.data[0].embedding}
