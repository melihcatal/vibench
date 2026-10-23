from openai import OpenAI
from model_client import get_text_client, resolve_embedding_model


def output_embedding(text: str, model: str | None = None) -> list[float]:
    client = get_text_client()
    model_name = resolve_embedding_model(model)
    response = client.embeddings.create(model=model_name, input=text)
    return response.data[0].embedding
