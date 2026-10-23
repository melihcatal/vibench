from openai import OpenAI


def moderation_reason_embedding(text, model="text-embedding-3-small"):
    client = OpenAI()
    response = client.embeddings.create(model=model, input=text)
    return response.data[0].embedding
