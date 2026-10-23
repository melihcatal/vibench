from openai import AzureOpenAI

from model_client import build_client


def platform_output_embedding(text: str) -> list[float]:
    client: AzureOpenAI = build_client()
    embedding = client.embeddings.create(model="text-embedding-3-small", input=text)
    return list(embedding.data[0].embedding)
