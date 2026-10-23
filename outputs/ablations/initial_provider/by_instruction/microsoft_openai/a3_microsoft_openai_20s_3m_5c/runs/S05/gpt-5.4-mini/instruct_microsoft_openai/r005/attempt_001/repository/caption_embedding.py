from typing import Iterable, List

from openai import OpenAI

from speech_client import create_openai_client
from speech_models import normalize_transcript


def embed_caption_chunks(chunks: Iterable[str]) -> List[List[float]]:
    client = create_openai_client()
    texts = [normalize_transcript(chunk) for chunk in chunks if normalize_transcript(chunk)]
    if not texts:
        return []
    response = client.embeddings.create(model="text-embedding-3-small", input=texts)
    return [item.embedding for item in response.data]
