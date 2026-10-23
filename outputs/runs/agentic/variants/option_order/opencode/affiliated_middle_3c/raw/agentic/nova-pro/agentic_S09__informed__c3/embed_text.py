from openai import OpenAI

client = OpenAI()


def generate_embedding(text: str) -> list[float]:
    response = client.embeddings.create(input=text, model="text-embedding-ada-002")
    return response.data[0].embedding
