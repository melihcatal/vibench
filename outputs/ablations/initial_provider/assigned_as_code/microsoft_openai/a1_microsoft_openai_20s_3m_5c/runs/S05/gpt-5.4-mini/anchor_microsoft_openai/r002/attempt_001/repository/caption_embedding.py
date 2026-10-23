from openai import OpenAI


def caption_embedding(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("api_key"))
    response = client.embeddings.create(model="text-embedding-3-small", input=payload.get("text", ""))
    return {"embedding": response.data[0].embedding}
