from openai import OpenAI


def caption_embedding(text: str):
    client = OpenAI()
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding
