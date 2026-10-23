from openai import OpenAI


def moderation_reason_embedding(text: str) -> list[float]:
    client = OpenAI()
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding
