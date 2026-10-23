from openai import OpenAI


def secret_audit_embedding(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("openai_api_key"))
    model = config.get("model", "text-embedding-3-small")
    text = payload.get("notes", "")
    response = client.embeddings.create(model=model, input=text)
    return {"embedding": response.data[0].embedding, "model": model}
