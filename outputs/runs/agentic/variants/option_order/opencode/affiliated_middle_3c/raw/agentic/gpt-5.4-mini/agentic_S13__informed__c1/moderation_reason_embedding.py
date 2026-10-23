from openai import OpenAI

client = OpenAI()
MODEL = 'text-embedding-3-large'


def moderation_reason_embedding(text):
    response = client.embeddings.create(model=MODEL, input=text)
    return response.data[0].embedding
