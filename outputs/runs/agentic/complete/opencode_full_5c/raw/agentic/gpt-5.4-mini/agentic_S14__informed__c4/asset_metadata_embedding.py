from openai import OpenAI


def asset_metadata_embedding(text: str, model: str = "text-embedding-3-small") -> dict:
    client = OpenAI()
    resp = client.embeddings.create(model=model, input=text)
    return {"model": model, "embedding": resp.data[0].embedding}
