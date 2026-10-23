import os

from openai import OpenAI

from speech_models import normalize_text


def embed_caption_chunks(chunks):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))
    texts = [normalize_text(chunk) for chunk in chunks]
    response = client.embeddings.create(model="text-embedding-3-small", input=texts)
    return [item.embedding for item in response.data]
