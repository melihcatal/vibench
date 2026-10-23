from openai import AzureOpenAI

from observability_client import _client


def log_embedding(message: str) -> list:
    client: AzureOpenAI = _client()
    response = client.embeddings.create(model="text-embedding-3-large", input=message)
    return response.data[0].embedding
