from openai import OpenAI

from model_client import get_client, normalize_text


def output_embedding(text: str):
    client = get_client()
    response = client.embeddings.create(model="text-embedding-3-small", input=normalize_text(text))
    return response.data[0].embedding
