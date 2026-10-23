from openai import OpenAI


def log_embedding(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config["api_key"], base_url=config.get("base_url"))
    model = config.get("model", "text-embedding-3-small")
    response = client.embeddings.create(model=model, input=payload["text"])
    return {"embedding": response.data[0].embedding, "model": model}
