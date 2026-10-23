from openai import OpenAI


def embed_caption_chunks(chunks: list[str]) -> list[list[float]]:
    client = OpenAI()
    response = client.embeddings.create(model="text-embedding-3-large", input=chunks)
    return [item.embedding for item in response.data]
