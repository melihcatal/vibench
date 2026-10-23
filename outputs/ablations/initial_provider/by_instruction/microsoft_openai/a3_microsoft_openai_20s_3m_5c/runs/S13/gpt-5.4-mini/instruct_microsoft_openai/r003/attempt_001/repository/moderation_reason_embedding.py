from openai import OpenAI


def moderation_reason_embedding(texts):
    client = OpenAI()
    return client.embeddings.create(model="text-embedding-3-small", input=texts)
