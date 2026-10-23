import os
from typing import List

from openai import OpenAI

from speech_client import load_config
from speech_models import normalize_transcript

EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def embed_caption_chunks(chunks: List[str]) -> List[List[float]]:
    client = OpenAI(api_key=load_config().api_key, base_url=load_config().base_url)
    cleaned = [normalize_transcript(c) for c in chunks if normalize_transcript(c)]
    if not cleaned:
        return []
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=cleaned)
    return [list(item.embedding) for item in response.data]
