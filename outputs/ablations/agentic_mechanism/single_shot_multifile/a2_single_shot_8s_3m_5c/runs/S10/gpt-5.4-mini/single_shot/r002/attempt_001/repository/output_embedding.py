from openai import OpenAI
from model_client import get_client, get_model_name


def output_embedding(text: str) -> list:
    client = get_client()
    model = get_model_name("embedding")
    response = client.embeddings.create(model=model, input=text)
    return response.data[0].embedding
