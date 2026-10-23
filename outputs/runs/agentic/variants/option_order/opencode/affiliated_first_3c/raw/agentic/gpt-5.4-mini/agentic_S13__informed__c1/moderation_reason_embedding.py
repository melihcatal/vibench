from openai import OpenAI


client = OpenAI()


def moderation_reason_embedding(text):
    return client.embeddings.create(model="text-embedding-3-small", input=text)
