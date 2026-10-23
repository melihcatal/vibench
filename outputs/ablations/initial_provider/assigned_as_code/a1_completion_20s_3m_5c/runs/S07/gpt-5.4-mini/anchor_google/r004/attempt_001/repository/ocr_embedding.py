from openai import OpenAI


def ocr_embedding(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config["api_key"])
    response = client.embeddings.create(model=config.get("model", "text-embedding-3-small"), input=payload["text"])
    return {"embedding": response.data[0].embedding}
