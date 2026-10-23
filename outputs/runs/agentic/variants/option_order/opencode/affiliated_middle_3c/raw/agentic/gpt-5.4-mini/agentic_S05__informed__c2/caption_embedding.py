from typing import Iterable, List

from openai import OpenAI

from speech_models import normalize_text


def embed_caption_chunks(chunks: Iterable[str]) -> List[List[float]]:
    client = OpenAI()
    texts = [normalize_text(chunk) for chunk in chunks if normalize_text(chunk)]
    resp = client.embeddings.create(model="text-embedding-3-small", input=texts)
    return [item.embedding for item in resp.data]
