from openai import OpenAI


def embed_message(text: str) -> list:
    client = OpenAI()
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding
