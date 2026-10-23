from openai import OpenAI


def caption_embedding(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("api_key"))
    response = client.embeddings.create(model=config.get("model", "text-embedding-3-small"), input=payload["text"])
    return {"text": payload["text"], "embedding": response.data[0].embedding, "is_final": payload.get("is_final", False)}
