from openai import OpenAI


def transcript_embedding(segments: list[str]) -> list[list[float]]:
    client = OpenAI()
    response = client.embeddings.create(model="text-embedding-3-large", input=segments)
    return [item.embedding for item in response.data]
