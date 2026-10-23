from openai import OpenAI

PROVIDER = "openai:text-embedding-3-small"


def embed_translated_segment(segment: str) -> dict:
    client = OpenAI()
    result = client.embeddings.create(model="text-embedding-3-small", input=segment)
    vector = result.data[0].embedding if result.data else []
    return {"vector": vector, "provider": PROVIDER}
