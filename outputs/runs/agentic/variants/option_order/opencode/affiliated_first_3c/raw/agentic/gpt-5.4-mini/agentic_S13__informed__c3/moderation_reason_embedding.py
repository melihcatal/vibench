from openai import OpenAI

client = OpenAI()


def moderation_reason_embedding(text, model="text-embedding-3-large"):
    resp = client.embeddings.create(model=model, input=text)
    return resp.data[0].embedding
