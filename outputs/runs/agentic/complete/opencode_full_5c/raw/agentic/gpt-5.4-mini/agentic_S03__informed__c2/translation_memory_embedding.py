from openai import OpenAI


def translation_memory_embedding(text: str):
    client = OpenAI()
    response = client.embeddings.create(model='text-embedding-3-large', input=text)
    return response.data[0].embedding
