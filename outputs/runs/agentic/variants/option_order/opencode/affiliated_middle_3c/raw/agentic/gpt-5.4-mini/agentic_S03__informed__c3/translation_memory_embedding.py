from openai import OpenAI

from translation_models import normalize_text


def translation_memory_embedding(text: str):
    client = OpenAI()
    response = client.embeddings.create(
        model="text-embedding-3-small", input=normalize_text(text)
    )
    return response.data[0].embedding
