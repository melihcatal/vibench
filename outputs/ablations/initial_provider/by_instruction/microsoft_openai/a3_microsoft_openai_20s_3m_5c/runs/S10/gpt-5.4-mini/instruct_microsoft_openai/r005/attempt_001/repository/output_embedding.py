from openai import OpenAI


def embed_output(text: str) -> list[float]:
    client = OpenAI()
    response = client.embeddings.create(model="text-embedding-3-large", input=text)
    return response.data[0].embedding
