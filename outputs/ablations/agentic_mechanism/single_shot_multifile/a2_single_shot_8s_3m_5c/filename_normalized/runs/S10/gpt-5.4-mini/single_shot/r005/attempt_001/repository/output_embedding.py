from openai import OpenAI
from model_client import get_client, get_model_name


def output_embedding(text: str) -> list[float]:
    client = get_client()
    model_name = get_model_name("embed")
    response = client.embeddings.create(model=model_name, input=text)
    return response.data[0].embedding
