from openai import OpenAI
from model_client import get_platform_client


def platform_output_embedding(text: str):
    client = get_platform_client()
    result = client.embeddings.create(model="text-embedding-3-small", input=text)
    return result.data[0].embedding
