from openai import OpenAI

from speech_models import normalize_text


def embed_script(text: str):
    client = OpenAI()
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=normalize_text(text),
    )
    return response.data[0].embedding
