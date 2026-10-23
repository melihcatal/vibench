from openai import OpenAI

from speech_models import normalize_payload


def script_embedding(payload, config=None):
    payload = normalize_payload(payload)
    config = dict(config or {})
    client = OpenAI(api_key=config.get("api_key"))
    response = client.embeddings.create(model=config.get("model", "text-embedding-3-small"), input=payload.get("text", ""))
    return {"embedding": response.data[0].embedding, "model": config.get("model", "text-embedding-3-small")}
