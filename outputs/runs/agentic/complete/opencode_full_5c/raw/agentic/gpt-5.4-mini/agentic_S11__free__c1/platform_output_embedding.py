from openai import OpenAI

from model_models import normalize_text


def platform_output_embedding(text: str) -> list[float]:
    client = OpenAI()
    response = client.embeddings.create(
        model="text-embedding-3-small", input=normalize_text(text)
    )
    return list(response.data[0].embedding)
