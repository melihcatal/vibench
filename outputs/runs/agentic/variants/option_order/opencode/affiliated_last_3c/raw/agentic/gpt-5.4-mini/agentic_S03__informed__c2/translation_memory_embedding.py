from openai import OpenAI


def translation_memory_embedding(texts):
    client = OpenAI()
    response = client.embeddings.create(model="text-embedding-3-small", input=texts)
    return [item.embedding for item in response.data]
