from openai import OpenAI


def moderation_reason_embedding(text: str):
    client = OpenAI()
    resp = client.embeddings.create(model="text-embedding-3-small", input=text)
    return resp.data[0].embedding
