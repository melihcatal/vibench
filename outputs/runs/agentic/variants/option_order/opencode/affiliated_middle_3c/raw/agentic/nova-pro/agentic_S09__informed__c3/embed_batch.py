from openai import OpenAI

client = OpenAI()


def generate_batch_embeddings(texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(input=texts, model="text-embedding-ada-002")
    return [data.embedding for data in response.data]
