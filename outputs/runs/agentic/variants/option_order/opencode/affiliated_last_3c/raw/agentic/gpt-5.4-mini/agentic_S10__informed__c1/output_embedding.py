from openai import OpenAI

from model_client import get_model_name, get_openai_client


def embed_output(text: str) -> list[float]:
    client: OpenAI = get_openai_client()
    response = client.embeddings.create(model=get_model_name("embedding"), input=text)
    return response.data[0].embedding
