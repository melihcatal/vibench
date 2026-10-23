from openai import OpenAI


def embed_caption_chunks(chunks):
    client = OpenAI()
    response = client.embeddings.create(model="text-embedding-3-small", input=chunks)
    return [item.embedding for item in response.data]
