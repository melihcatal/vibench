from openai import OpenAI
from model_client import get_chat_client


def output_embedding(text: str) -> list:
    client = get_chat_client()
    response = client.embeddings.create(model='text-embedding-3-small', input=text)
    data = getattr(response, 'data', [])
    if not data:
        return []
    return list(getattr(data[0], 'embedding', []))
